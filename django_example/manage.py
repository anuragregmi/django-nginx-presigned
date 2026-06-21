#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root / "src"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
