from datetime import datetime

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
            print("Ошибка: неверный формат. Используйте ГГГГ-ММ-ДД (например, 2026-09-20).")