from urllib.parse import parse_qs, urlsplit

import pytest
from django.core import signing
from django.test import override_settings

from nginx_presign import generate_presigned_url
from nginx_presign.conf import get_signing_salt
from nginx_presign.paths import normalize_media_path


def _token_from_url(url):
    query = parse_qs(urlsplit(url).query)
    return query["token"][0]


def test_generate_presigned_url_uses_configured_absolute_base_url():
    url = generate_presigned_url("/media/uploads/report.pdf")

    parsed = urlsplit(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "cdn.example.test"
    assert parsed.path == "/nginx-presign/uploads/report.pdf"

    payload = signing.loads(_token_from_url(url), salt=get_signing_salt(), max_age=300)
    assert payload["path"] == "uploads/report.pdf"
    assert isinstance(payload["exp"], int)


def test_generate_presigned_url_supports_base_url_override():
    url = generate_presigned_url("uploads/report.pdf", base_url="https://files.example.test/root")

    parsed = urlsplit(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "files.example.test"
    assert parsed.path == "/root/nginx-presign/uploads/report.pdf"


@override_settings(NGINX_PRESIGN_ROUTE_PATH="private-media")
def test_generate_presigned_url_uses_configured_route_path():
    assert urlsplit(generate_presigned_url("uploads/report.pdf")).path == "/private-media/uploads/report.pdf"


def test_generate_presigned_url_preserves_quoted_filename_extension():
    url = generate_presigned_url("uploads/my report.final.pdf")

    assert urlsplit(url).path == "/nginx-presign/uploads/my%20report.final.pdf"


@pytest.mark.parametrize(
    ("input_path", "expected"),
    [
        ("uploads/report.pdf", "uploads/report.pdf"),
        ("/media/uploads/report.pdf", "uploads/report.pdf"),
        ("https://assets.example.test/media/uploads/report.pdf?download=1", "uploads/report.pdf"),
        ("nested//report.pdf", "nested/report.pdf"),
    ],
)
def test_normalize_media_path_accepts_media_paths(input_path, expected):
    assert normalize_media_path(input_path) == expected


@pytest.mark.parametrize(
    "input_path",
    [
        "",
        "/media/",
        "/var/www/media/secret.pdf",
        "../secret.pdf",
        "/media/../secret.pdf",
        "nested\\secret.pdf",
    ],
)
def test_normalize_media_path_rejects_unsafe_paths(input_path):
    with pytest.raises(ValueError):
        normalize_media_path(input_path)


def test_generate_presigned_url_rejects_non_positive_expiry():
    with pytest.raises(ValueError, match="expires_in"):
        generate_presigned_url("uploads/report.pdf", expires_in=0)


@override_settings(NGINX_PRESIGN_BASE_URL=None)
def test_generate_presigned_url_requires_base_url():
    with pytest.raises(ValueError, match="NGINX_PRESIGN_BASE_URL"):
        generate_presigned_url("uploads/report.pdf")
