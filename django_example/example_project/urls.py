from django.http import HttpResponse
from django.urls import include, path

from nginx_presign import generate_presigned_url


def index(request):
    signed_url = generate_presigned_url("/media/test/hello.txt", expires_in=10)
    return HttpResponse(
        "\n".join(
            [
                "<!doctype html>",
                "<title>nginx-presign example</title>",
                "<h1>nginx-presign example</h1>",
                f'<p><a href="{signed_url}">Open signed sample file</a></p>',
                f"<p><code>{signed_url}</code></p>",
            ]
        )
    )


urlpatterns = [
    path("", index, name="index"),
    path("media/", include("nginx_presign.urls")),
]
