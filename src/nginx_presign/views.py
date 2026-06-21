from __future__ import annotations

from django.core import signing
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import timezone
from django.views.static import serve as serve_static

from .conf import get_dev_document_root, get_dev_serve_enabled, get_internal_prefix, get_signing_salt
from .paths import build_internal_uri


def serve_presigned_media(request):
    if request.method not in ("GET", "HEAD"):
        return HttpResponseNotAllowed(["GET", "HEAD"])

    token = request.GET.get("token")
    if not token:
        return HttpResponseBadRequest("Missing token")

    try:
        payload = signing.loads(token, salt=get_signing_salt())
        relative_path = payload["path"]
        expires_at = int(payload["exp"])
        if expires_at <= int(timezone.now().timestamp()):
            return HttpResponseForbidden("Expired token")
        if get_dev_serve_enabled():
            return serve_static(request, relative_path, document_root=get_dev_document_root())
        internal_uri = build_internal_uri(relative_path, get_internal_prefix())
    except signing.BadSignature:
        return HttpResponseForbidden("Invalid token")
    except (KeyError, TypeError, ValueError, OverflowError):
        return HttpResponseBadRequest("Invalid token payload")

    response = HttpResponse()
    response["X-Accel-Redirect"] = internal_uri
    return response
