"""Модуль валидации данных."""

from utils.constants import MIN_TABLE_NUMBER


class Validator:
    """Класс для валидации данных."""

    @staticmethod
    def validate_table_number(table_number: int) -> None:
        """Проверить номер стола."""
        if not isinstance(table_number, int) or table_number < MIN_TABLE_NUMBER:
            raise ValueError(
                f"Номер стола должен быть положительным числом (>= {MIN_TABLE_NUMBER})")

    @staticmethod
    def validate_customer_name(name: str) -> None:
        """Проверить имя клиента."""
        if not name or not name.strip():
            raise ValueError("Имя клиента не может быть пустым")

    @staticmethod
    def validate_time(time: str) -> None:
        """Проверить время бронирования."""
        if not time:
            raise ValueError("Время не может быть пустым")

    @staticmethod
    def validate_price(price: float) -> None:
        """Проверить цену."""
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
