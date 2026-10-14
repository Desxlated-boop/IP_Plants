#!/usr/bin/env python
"""Утилита командной строки Django для управления проектом."""
import os
import sys


def main() -> None:
    """Запустить административные команды Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantly.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Активировано ли "
            "виртуальное окружение и установлен ли Django?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
