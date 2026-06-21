# AGENTS.md

## Project Overview

This repository contains `django-nginx-presign`, a small Django package for
generating expiring media URLs that are validated by Django and served through
Nginx `X-Accel-Redirect`.

## Development Commands

- Run tests with `.venv/bin/python -m pytest`.
- Install local dependencies with `.venv/bin/python -m pip install 'Django>=4.2' 'pytest>=8' 'pytest-django>=4.8'`.
- Build/install the package locally with `.venv/bin/python -m pip install .`.

## Code Conventions

- Keep the public API small; `generate_presigned_url` is the main package-level
  helper.
- Keep production serving on `X-Accel-Redirect` by default.
- Keep `NGINX_PRESIGN_DEV_SERVE` explicitly opt-in and development-only.
- Validate media paths carefully; reject traversal, backslashes, empty paths,
  and filesystem-looking absolute paths outside `MEDIA_URL`.
- Do not make Django check file existence in production mode.

## Testing Notes

- Add tests for any behavior affecting signing, expiry, path normalization, or
  response mode selection.
- Use Django test settings from `tests/settings.py`.
- For dev serving tests, use `tmp_path` and override `MEDIA_ROOT`.
