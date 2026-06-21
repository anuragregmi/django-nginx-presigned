from __future__ import annotations

import posixpath
from urllib.parse import unquote, urlsplit

from django.conf import settings


def normalize_media_path(file_url: str) -> str:
    """Normalize a caller-provided media URL/path to a safe relative path."""
    if not isinstance(file_url, str):
        raise TypeError("file_url must be a string")

    value = file_url.strip()
    if not value:
        raise ValueError("file_url cannot be empty")

    parsed = urlsplit(value)
    path = parsed.path if parsed.scheme or parsed.netloc else value
    path = unquote(path.split("?", 1)[0].split("#", 1)[0])
    had_leading_slash = path.startswith("/")
    stripped_media_prefix = False

    media_url = getattr(settings, "MEDIA_URL", "")
    if media_url:
        media_path = urlsplit(str(media_url)).path
        if media_path and media_path != "/":
            media_path = _ensure_trailing_slash(media_path)
            if path == media_path.rstrip("/"):
                path = ""
                stripped_media_prefix = True
            elif path.startswith(media_path):
                path = path[len(media_path) :]
                stripped_media_prefix = True

    if path.startswith("/"):
        if had_leading_slash and not stripped_media_prefix:
            raise ValueError("absolute paths must begin with MEDIA_URL")
        path = path.lstrip("/")

    return _validate_relative_path(path)


def build_internal_uri(relative_path: str, internal_prefix: str) -> str:
    clean_path = _validate_relative_path(relative_path)
    return _ensure_trailing_slash(internal_prefix) + clean_path


def _validate_relative_path(path: str) -> str:
    if "\\" in path:
        raise ValueError("file_url cannot contain backslashes")

    cleaned = posixpath.normpath(path)
    if cleaned in ("", "."):
        raise ValueError("file_url must point to a media file")
    if cleaned.startswith("../") or cleaned == "..":
        raise ValueError("file_url cannot contain parent directory traversal")
    if cleaned.startswith("/"):
        raise ValueError("file_url must be relative to media root")

    return cleaned


def _ensure_trailing_slash(path: str) -> str:
    return path if path.endswith("/") else path + "/"
