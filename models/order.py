"""Модуль с классом Order."""

from services.validator import Validator
from utils.constants import CURRENCY_SYMBOL


class Order:
    """Класс для представления заказа."""

    def __init__(self, table_number: int) -> None:
        Validator.validate_table_number(table_number)
        self.table_number = table_number
        self._items = []
        self._total = 0.0

    @property
    def items(self):
        """Получить список позиций (копия)."""
        return self._items.copy()

    @property
    def total(self) -> float:
        """Получить общую сумму."""
        return self._total

    def add_item(self, menu_item) -> None:
        """Добавить позицию в заказ."""
        self._items.append(menu_item)
        self._total += menu_item.price

    def remove_item(self, index: int) -> None:
        """Удалить позицию из заказа по индексу."""
        if 0 <= index < len(self._items):
            removed = self._items.pop(index)
            self._total -= removed.price
        else:
            raise IndexError("Неверный индекс позиции")

    def get_order_summary(self) -> str:
        """Получить сводку заказа."""
        if not self._items:
            return f"Заказ для стола {self.table_number}: нет позиций"

        summary = f"Заказ для стола {self.table_number}:\n"
        for item in self._items:
            summary += f"  - {item.name}: {item.price}{CURRENCY_SYMBOL}\n"
        summary += f"Итого: {self._total}{CURRENCY_SYMBOL}"
        return summary

    def __len__(self) -> int:
        """Количество позиций."""
        return len(self._items)
