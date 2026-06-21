# django-nginx-presign

Small Django package for generating expiring media URLs that are validated by
Django and served by Nginx through `X-Accel-Redirect`.

## Install

```bash
pip install django-nginx-presign
```

## Django setup

```python
INSTALLED_APPS = [
    "nginx_presign",
]

MEDIA_URL = "/media/"

NGINX_PRESIGN_BASE_URL = "https://example.com"
NGINX_PRESIGN_INTERNAL_PREFIX = "/protected-media/"
NGINX_PRESIGN_DEFAULT_EXPIRES_IN = 300
```

Add the validation endpoint:

```python
from django.urls import include, path

urlpatterns = [
    path("nginx-presign/", include("nginx_presign.urls")),
]
```

Generate an absolute expiring URL:

```python
from nginx_presign import generate_presigned_url

url = generate_presigned_url("/media/uploads/report.pdf", expires_in=600)
```

The generated URL points to Django. After validation, Django returns an empty
response with `X-Accel-Redirect`, and Nginx serves the file internally.

## Development mode

When developing without Nginx, enable direct Django file serving:

```python
DEBUG = True
MEDIA_ROOT = BASE_DIR / "media"
NGINX_PRESIGN_DEV_SERVE = True
```

With this enabled, the same signed URL is still validated by Django, but the
view serves the file from `MEDIA_ROOT` instead of returning `X-Accel-Redirect`.
Keep this setting disabled in production.

## Nginx setup

```nginx
location /protected-media/ {
    internal;
    alias /path/to/media/root/;
}
```

The `alias` directory should match your Django media root. The internal prefix
must match `NGINX_PRESIGN_INTERNAL_PREFIX`.

## Settings

| Setting | Default | Description |
| --- | --- | --- |
| `NGINX_PRESIGN_BASE_URL` | required | Public scheme and host used for generated absolute URLs. |
| `NGINX_PRESIGN_ROUTE_PATH` | `/nginx-presign/` | Public Django validation route. |
| `NGINX_PRESIGN_INTERNAL_PREFIX` | `/protected-media/` | Internal Nginx location prefix. |
| `NGINX_PRESIGN_DEFAULT_EXPIRES_IN` | `300` | Default URL lifetime in seconds. |
| `NGINX_PRESIGN_SIGNING_SALT` | package salt | Salt used with Django signing. |
| `NGINX_PRESIGN_DEV_SERVE` | `False` | Serve files from `MEDIA_ROOT` in local development instead of using Nginx. |

## API

```python
generate_presigned_url(file_url, expires_in=None, *, base_url=None) -> str
```

`file_url` can be a media-relative path, a path beginning with `MEDIA_URL`, or a
full URL whose path begins with `MEDIA_URL`.

Unsafe paths are rejected, including empty paths, filesystem absolute paths,
backslash paths, and `..` traversal.
