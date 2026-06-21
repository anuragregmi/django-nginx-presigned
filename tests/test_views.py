from datetime import timedelta

import pytest
from django.core import signing
from django.test import Client, override_settings
from django.utils import timezone

from nginx_presign import generate_presigned_url
from nginx_presign.conf import get_signing_salt


def _client_path_from_absolute_url(url):
    return url.removeprefix("https://cdn.example.test")


def test_valid_token_returns_x_accel_redirect():
    url = generate_presigned_url("/media/uploads/report.pdf")
    response = Client().get(_client_path_from_absolute_url(url))

    assert response.status_code == 200
    assert response["X-Accel-Redirect"] == "/protected-media/uploads/report.pdf"
    assert response.content == b""


def test_head_request_returns_x_accel_redirect():
    url = generate_presigned_url("/media/uploads/report.pdf")
    response = Client().head(_client_path_from_absolute_url(url))

    assert response.status_code == 200
    assert response["X-Accel-Redirect"] == "/protected-media/uploads/report.pdf"


def test_missing_token_returns_400():
    response = Client().get("/nginx-presign/uploads/report.pdf")

    assert response.status_code == 400


def test_tampered_token_returns_403():
    url = _client_path_from_absolute_url(generate_presigned_url("/media/uploads/report.pdf"))
    response = Client().get(url + "tampered")

    assert response.status_code == 403


def test_post_returns_405():
    response = Client().post("/nginx-presign/")

    assert response.status_code == 405


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"path": "../secret.pdf"},
        {"path": "nested\\secret.pdf"},
    ],
)
def test_invalid_signed_payload_returns_400(payload):
    token = signing.dumps(payload, salt=get_signing_salt())
    response = Client().get("/nginx-presign/uploads/report.pdf", {"token": token})

    assert response.status_code == 400


def test_signed_path_mismatch_returns_403():
    url = generate_presigned_url("/media/uploads/report.pdf")
    response = Client().get(_client_path_from_absolute_url(url).replace("report.pdf", "other.pdf"))

    assert response.status_code == 403


def test_expired_token_returns_403(monkeypatch):
    now = timezone.now()
    monkeypatch.setattr(timezone, "now", lambda: now)
    url = generate_presigned_url("/media/uploads/report.pdf", expires_in=1)

    monkeypatch.setattr(timezone, "now", lambda: now + timedelta(seconds=2))

    response = Client().get(_client_path_from_absolute_url(url))

    assert response.status_code == 403


@override_settings(NGINX_PRESIGN_DEFAULT_EXPIRES_IN=1)
def test_per_call_expiry_can_exceed_default(monkeypatch):
    now = timezone.now()
    monkeypatch.setattr(timezone, "now", lambda: now)
    url = generate_presigned_url("/media/uploads/report.pdf", expires_in=10)

    monkeypatch.setattr(timezone, "now", lambda: now + timedelta(seconds=2))

    response = Client().get(_client_path_from_absolute_url(url))

    assert response.status_code == 200


@override_settings(NGINX_PRESIGN_DEV_SERVE=True)
def test_dev_serve_returns_file_from_media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    media_file = tmp_path / "uploads" / "report.txt"
    media_file.parent.mkdir()
    media_file.write_text("local dev file", encoding="utf-8")

    url = generate_presigned_url("/media/uploads/report.txt")
    response = Client().get(_client_path_from_absolute_url(url))

    assert response.status_code == 200
    assert b"".join(response.streaming_content) == b"local dev file"
    assert "X-Accel-Redirect" not in response


@override_settings(NGINX_PRESIGN_DEV_SERVE=True)
def test_dev_serve_missing_file_returns_404(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path

    url = generate_presigned_url("/media/uploads/missing.txt")
    response = Client().get(_client_path_from_absolute_url(url))

    assert response.status_code == 404
