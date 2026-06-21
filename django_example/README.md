# Django Example

Tiny Django project for manually testing `django-nginx-presign`.

Run it from the repository root:

```bash
.venv/bin/python django_example/manage.py runserver
```

Open:

- `http://127.0.0.1:8000/` to see a generated signed URL.
- `http://127.0.0.1:8000/media/filename.extension?token=...` through the generated link
  to validate and serve the sample file.

This example enables:

```python
NGINX_PRESIGN_DEV_SERVE = True
```

so Django serves files from `django_example/media` instead of requiring Nginx.
