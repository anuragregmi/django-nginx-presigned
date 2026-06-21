from __future__ import annotations

from datetime import timedelta
from urllib.parse import quote, urlencode, urljoin

from django.core import signing
from django.utils import timezone

from .conf import get_base_url, get_default_expires_in, get_route_path, get_signing_salt
from .paths import normalize_media_path


def generate_presigned_url(file_url: str, expires_in: int | None = None, *, base_url: str | None = None) -> str:
    """Return an absolute, expiring URL for a media file."""
    relative_path = normalize_media_path(file_url)
    max_age = get_default_expires_in() if expires_in is None else expires_in

    if max_age <= 0:
        raise ValueError("expires_in must be a positive integer")

    expires_at = timezone.now() + timedelta(seconds=max_age)
    payload = {"path": relative_path, "exp": int(expires_at.timestamp())}
    token = signing.dumps(payload, salt=get_signing_salt())

    public_base_url = get_base_url(base_url)
    route_path = get_route_path()
    route_url = urljoin(public_base_url.rstrip("/") + "/", route_path.lstrip("/"))
    query_string = urlencode({"token": token}, quote_via=quote)
    return f"{route_url}?{query_string}"
