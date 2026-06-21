from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

SECRET_KEY = "django-example-dev-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

ROOT_URLCONF = "example_project.urls"
WSGI_APPLICATION = "example_project.wsgi.application"
ASGI_APPLICATION = "example_project.asgi.application"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "nginx_presign",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NGINX_PRESIGN_BASE_URL = "http://127.0.0.1:8000"
NGINX_PRESIGN_INTERNAL_PREFIX = "/protected-media/"
NGINX_PRESIGN_DEFAULT_EXPIRES_IN = 300
NGINX_PRESIGN_DEV_SERVE = True
NGINX_PRESIGN_ROUTE_PATH="/media"
