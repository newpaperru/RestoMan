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
        self.table_number = table_number
        self.items = []
        self.total = 0

    def add_item(self, menu_item: MenuItem) -> None:
        """Добавить позицию в заказ."""
        self.items.append(menu_item)
        self.total += menu_item.price

    def get_order_summary(self) -> str:
        """Получить сводку заказа."""
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
        item = MenuItem(name, price, category)
        self.menu.append(item)
        return item

    def create_order(self, table_number: int) -> Order:
        """Создать новый заказ."""
        order = Order(table_number)
        self.orders.append(order)
        return order

    def book_table(self, customer_name: str, table_number: int, time: str) -> dict:
        """Забронировать столик."""
        booking = {
            'customer': customer_name,
            'table': table_number,
            'time': time
        }
        self.bookings.append(booking)
        return booking

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


if __name__ == "__main__":
    main()
