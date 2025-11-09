#!/usr/bin/env python
import warnings

# Suppress development server warning
warnings.filterwarnings(
    "ignore",
    message=".*This is a development server.*",
)

import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_ai_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
