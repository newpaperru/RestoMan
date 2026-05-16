"""Restaurant Management System."""

from models.restaurant_manager import RestaurantManager
from utils.constants import CURRENCY_SYMBOL


def main() -> None:
    """Демонстрационная функция."""
    rm = RestaurantManager()

    # Добавляем блюда
    rm.add_menu_item("Борщ", 5.99, "Суп")
    rm.add_menu_item("Цезарь", 7.99, "Салат")
    rm.add_menu_item("Стейк", 15.99, "Горячее")

    print("Меню ресторана:")
    for item in rm.get_menu_list():
        print(f"  {item}")

    # Создаем заказ
    order = rm.create_order(5)
    order.add_item(rm.menu[0])
    order.add_item(rm.menu[2])

    print("\n" + order.get_order_summary())
    print(f"\nОбщая выручка: {rm.get_total_revenue()}{CURRENCY_SYMBOL}")


if __name__ == "__main__":
    main()
