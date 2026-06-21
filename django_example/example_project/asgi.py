import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application


repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root / "src"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

application = get_asgi_application()
