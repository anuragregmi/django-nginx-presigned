from django.urls import include, path

urlpatterns = [
    path("nginx-presign/", include("nginx_presign.urls")),
]
