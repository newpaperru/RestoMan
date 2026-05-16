"""
Restaurant Management System
"""


class MenuItem:
    """Класс для представления позиции меню."""

    def __init__(self, name: str, price: float, category: str) -> None:
        self.name = name
        self.price = price
        self.category = category

    def get_info(self) -> str:
        """Получить информацию о блюде."""
        return f"{self.name} ({self.category}) - {self.price}₽"


class Order:
    """Класс для представления заказа."""

    def __init__(self, table_number: int) -> None:
        if table_number <= 0:
            raise ValueError("Номер стола должен быть положительным числом")
        self.table_number = table_number
        self.items = []
        self.total = 0

    def add_item(self, menu_item: MenuItem) -> None:
        """Добавить позицию в заказ."""
        self.items.append(menu_item)
        self.total += menu_item.price

    def remove_item(self, index: int) -> None:
        """Удалить позицию из заказа по индексу."""
        if 0 <= index < len(self.items):
            removed = self.items.pop(index)
            self.total -= removed.price
        else:
            raise IndexError("Неверный индекс позиции")

    def get_order_summary(self) -> str:
        """Получить сводку заказа."""
        if not self.items:
            return f"Заказ для стола {self.table_number}: нет позиций"

        summary = f"Заказ для стола {self.table_number}:\n"
        for item in self.items:
            summary += f"  - {item.name}: {item.price}₽\n"
        summary += f"Итого: {self.total}₽"
        return summary


class RestaurantManager:
    """Основной класс для управления рестораном."""

    def __init__(self) -> None:
        self.menu = []
        self.orders = []
        self.bookings = []

    def add_menu_item(self, name: str, price: float, category: str) -> MenuItem:
        """Добавить позицию в меню."""
        # Проверка на дублирование
        for item in self.menu:
            if item.name.lower() == name.lower():
                raise ValueError(f"Блюдо '{name}' уже существует в меню")

        item = MenuItem(name, price, category)
        self.menu.append(item)
        return item

    def remove_menu_item(self, name: str) -> bool:
        """Удалить блюдо из меню по названию."""
        for i, item in enumerate(self.menu):
            if item.name.lower() == name.lower():
                self.menu.pop(i)
                return True
        return False

    def edit_menu_item_price(self, name: str, new_price: float) -> bool:
        """Изменить цену блюда."""
        for item in self.menu:
            if item.name.lower() == name.lower():
                item.price = new_price
                return True
        return False

    def create_order(self, table_number: int) -> Order:
        """Создать новый заказ."""
        if table_number <= 0:
            raise ValueError("Номер стола должен быть положительным")
        order = Order(table_number)
        self.orders.append(order)
        return order

    def book_table(self, customer_name: str, table_number: int, time: str) -> dict:
        """Забронировать столик."""
        if not customer_name:
            raise ValueError("Имя клиента не может быть пустым")
        if table_number <= 0:
            raise ValueError("Номер стола должен быть положительным")
        if not time:
            raise ValueError("Время не может быть пустым")

        # Проверка на уже существующую бронь на это время
        for booking in self.bookings:
            if (booking['table'] == table_number and
                booking['time'] == time and
                    booking.get('status') == 'active'):
                raise ValueError(f"Стол {table_number} уже забронирован на {time}")

        booking = {
            'customer': customer_name,
            'table': table_number,
            'time': time,
            'status': 'active'
        }
        self.bookings.append(booking)
        return booking

    def cancel_booking(self, customer_name: str, table_number: int, time: str) -> bool:
        """Отменить бронирование."""
        for booking in self.bookings:
            if (booking['customer'] == customer_name and
                booking['table'] == table_number and
                booking['time'] == time and
                    booking.get('status') == 'active'):
                booking['status'] = 'cancelled'
                return True
        return False

    def get_active_bookings(self) -> list:
        """Получить список активных бронирований."""
        return [b for b in self.bookings if b.get('status') == 'active']

    def get_menu_list(self) -> list:
        """Получить список меню."""
        return [item.get_info() for item in self.menu]

    def get_total_revenue(self) -> float:
        """Подсчитать общую выручку."""
        return sum(order.total for order in self.orders)


def main() -> None:
    """Демонстрационная функция."""
    rm = RestaurantManager()

    rm.add_menu_item("Борщ", 5.99, "Суп")
    rm.add_menu_item("Цезарь", 7.99, "Салат")
    rm.add_menu_item("Стейк", 15.99, "Горячее")

    print("Меню ресторана:")
    for item in rm.get_menu_list():
        print(f"  {item}")

    order = rm.create_order(5)
    order.add_item(rm.menu[0])
    order.add_item(rm.menu[2])

    print("\n" + order.get_order_summary())
    print(f"\nОбщая выручка: {rm.get_total_revenue()}₽")


if __name__ == "__main__":
    main()
