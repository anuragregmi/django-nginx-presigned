from django.urls import path

from .views import serve_presigned_media

urlpatterns = [
    path("", serve_presigned_media, name="nginx_presign_media"),
    path("<path:signed_path>", serve_presigned_media, name="nginx_presign_media_file"),
]
