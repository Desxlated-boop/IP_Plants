"""Вспомогательные функции: безопасный ввод и генерация идентификаторов."""
from datetime import datetime
from typing import Any, Iterable


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с обработкой ошибок."""
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)
        except ValueError:
            print("Ошибка: пожалуйста, введите целое число.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        user_input = input(prompt)
        try:
            # Проверяем, что дата корректна
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print(
                "Ошибка: формат ГГГГ-ММ-ДД (пример: 2026-09-20).")


def next_id(items: Iterable[Any]) -> int:
    """Вернуть следующий свободный числовой идентификатор."""
    return max((item.id for item in items), default=0) + 1
