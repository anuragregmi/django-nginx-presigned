SECRET_KEY = "tests-secret-key"
ROOT_URLCONF = "tests.urls"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
INSTALLED_APPS = [
    "nginx_presign",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = "/tmp/nginx-presign-tests-media"
NGINX_PRESIGN_BASE_URL = "https://cdn.example.test"
NGINX_PRESIGN_INTERNAL_PREFIX = "/protected-media/"
NGINX_PRESIGN_DEFAULT_EXPIRES_IN = 300
ALLOWED_HOSTS = ["testserver", "cdn.example.test"]
MIDDLEWARE = []
