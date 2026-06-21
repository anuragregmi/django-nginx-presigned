from __future__ import annotations

from django.conf import settings


DEFAULT_ROUTE_PATH = "/nginx-presign/"
DEFAULT_INTERNAL_PREFIX = "/protected-media/"
DEFAULT_EXPIRES_IN = 300
DEFAULT_SIGNING_SALT = "nginx_presign.media"
DEFAULT_DEV_SERVE = False


def get_base_url(override: str | None = None) -> str:
    base_url = override or getattr(settings, "NGINX_PRESIGN_BASE_URL", None)
    if not base_url:
        raise ValueError("NGINX_PRESIGN_BASE_URL must be configured or base_url must be passed")
    return str(base_url)


def get_route_path() -> str:
    return _slash_wrap(getattr(settings, "NGINX_PRESIGN_ROUTE_PATH", DEFAULT_ROUTE_PATH))


def get_internal_prefix() -> str:
    return _slash_wrap(getattr(settings, "NGINX_PRESIGN_INTERNAL_PREFIX", DEFAULT_INTERNAL_PREFIX))


def get_dev_serve_enabled() -> bool:
    return bool(getattr(settings, "NGINX_PRESIGN_DEV_SERVE", DEFAULT_DEV_SERVE))


def get_dev_document_root() -> str:
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        raise ValueError("MEDIA_ROOT must be configured when NGINX_PRESIGN_DEV_SERVE is enabled")
    return str(media_root)


def get_default_expires_in() -> int:
    value = getattr(settings, "NGINX_PRESIGN_DEFAULT_EXPIRES_IN", DEFAULT_EXPIRES_IN)
    try:
        expires_in = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("NGINX_PRESIGN_DEFAULT_EXPIRES_IN must be an integer") from exc

    if expires_in <= 0:
        raise ValueError("NGINX_PRESIGN_DEFAULT_EXPIRES_IN must be a positive integer")
    return expires_in


def get_signing_salt() -> str:
    return str(getattr(settings, "NGINX_PRESIGN_SIGNING_SALT", DEFAULT_SIGNING_SALT))


def _slash_wrap(value: str) -> str:
    path = str(value)
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path
