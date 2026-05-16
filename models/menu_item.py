"""Модуль с классом MenuItem."""

from utils.constants import CURRENCY_SYMBOL


class MenuItem:
    """Класс для представления позиции меню."""

    def __init__(self, name: str, price: float, category: str) -> None:
        self.name = name
        self.price = price
        self.category = category

    def get_info(self) -> str:
        """Получить информацию о блюде."""
        return f"{self.name} ({self.category}) - {self.price}{CURRENCY_SYMBOL}"

    def update_price(self, new_price: float) -> None:
        """Обновить цену блюда."""
        self.price = new_price
