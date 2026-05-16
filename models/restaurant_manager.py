"""Модуль с классом RestaurantManager."""

from models.menu_item import MenuItem
from models.order import Order
from services.validator import Validator
from utils.constants import BOOKING_STATUS_ACTIVE, BOOKING_STATUS_CANCELLED


class RestaurantManager:
    """Основной класс для управления рестораном."""

    def __init__(self) -> None:
        self._menu = []
        self._orders = []
        self._bookings = []

    @property
    def menu(self):
        """Получить копию меню."""
        return self._menu.copy()

    @property
    def orders(self):
        """Получить копию заказов."""
        return self._orders.copy()

    @property
    def bookings(self):
        """Получить копию бронирований."""
        return self._bookings.copy()

    # ========== Управление меню ==========
    def _find_menu_item(self, name: str):
        """Внутренний метод поиска блюда (убирает дублирование)."""
        for item in self._menu:
            if item.name.lower() == name.lower():
                return item
        return None

    def _find_menu_item_index(self, name: str):
        """Внутренний метод поиска индекса блюда."""
        for i, item in enumerate(self._menu):
            if item.name.lower() == name.lower():
                return i
        return -1

    def add_menu_item(self, name: str, price: float, category: str) -> MenuItem:
        """Добавить позицию в меню."""
        if self._find_menu_item(name):
            raise ValueError(f"Блюдо '{name}' уже существует в меню")

        Validator.validate_price(price)
        item = MenuItem(name, price, category)
        self._menu.append(item)
        return item

    def remove_menu_item(self, name: str) -> bool:
        """Удалить блюдо из меню по названию."""
        index = self._find_menu_item_index(name)
        if index != -1:
            self._menu.pop(index)
            return True
        return False

    def edit_menu_item_price(self, name: str, new_price: float) -> bool:
        """Изменить цену блюда."""
        item = self._find_menu_item(name)
        if item:
            Validator.validate_price(new_price)
            item.update_price(new_price)
            return True
        return False

    def get_menu_list(self) -> list:
        """Получить список меню."""
        return [item.get_info() for item in self._menu]

    # ========== Управление заказами ==========
    def create_order(self, table_number: int) -> Order:
        """Создать новый заказ."""
        Validator.validate_table_number(table_number)
        order = Order(table_number)
        self._orders.append(order)
        return order

    def get_total_revenue(self) -> float:
        """Подсчитать общую выручку."""
        return sum(order.total for order in self._orders)

    # ========== Управление бронированием ==========
    def _find_booking(self, customer_name: str, table_number: int, time: str):
        """Внутренний метод поиска бронирования."""
        for booking in self._bookings:
            if (booking['customer'] == customer_name and
                booking['table'] == table_number and
                    booking['time'] == time):
                return booking
        return None

    def book_table(self, customer_name: str, table_number: int, time: str) -> dict:
        """Забронировать столик."""
        Validator.validate_customer_name(customer_name)
        Validator.validate_table_number(table_number)
        Validator.validate_time(time)

        # Проверка на уже существующую бронь
        for booking in self._bookings:
            if (booking['table'] == table_number and
                booking['time'] == time and
                    booking.get('status') == BOOKING_STATUS_ACTIVE):
                raise ValueError(f"Стол {table_number} уже забронирован на {time}")

        booking = {
            'customer': customer_name.strip(),
            'table': table_number,
            'time': time,
            'status': BOOKING_STATUS_ACTIVE
        }
        self._bookings.append(booking)
        return booking

    def cancel_booking(self, customer_name: str, table_number: int, time: str) -> bool:
        """Отменить бронирование."""
        booking = self._find_booking(customer_name, table_number, time)
        if booking and booking.get('status') == BOOKING_STATUS_ACTIVE:
            booking['status'] = BOOKING_STATUS_CANCELLED
            return True
        return False

    def get_active_bookings(self) -> list:
        """Получить список активных бронирований."""
        return [b for b in self._bookings if b.get('status') == BOOKING_STATUS_ACTIVE]
