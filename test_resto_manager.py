import unittest
from resto_manager import MenuItem, Order, RestaurantManager


class TestRestaurantManager(unittest.TestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.rm = RestaurantManager()
        self.rm.add_menu_item("Пицца", 12.99, "Основное")
        self.rm.add_menu_item("Салат", 6.99, "Салат")

    def test_add_menu_item(self):
        """Тест добавления блюда в меню"""
        item = self.rm.add_menu_item("Суп", 4.99, "Первое")
        self.assertEqual(item.name, "Суп")
        self.assertEqual(item.price, 4.99)
        self.assertEqual(len(self.rm.menu), 3)

    def test_menu_item_info(self):
        """Тест получения информации о блюде"""
        item = MenuItem("Паста", 10.99, "Паста")
        self.assertEqual(item.get_info(), "Паста (Паста) - 10.99₽")

    def test_create_order(self):
        """Тест создания заказа"""
        order = self.rm.create_order(3)
        self.assertEqual(order.table_number, 3)
        self.assertEqual(len(self.rm.orders), 1)

    def test_add_item_to_order(self):
        """Тест добавления блюда в заказ"""
        order = Order(1)
        menu_item = MenuItem("Кофе", 2.99, "Напиток")
        order.add_item(menu_item)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.total, 2.99)

    def test_order_summary(self):
        """Тест формирования сводки заказа"""
        order = Order(2)
        order.add_item(MenuItem("Чай", 1.99, "Напиток"))
        order.add_item(MenuItem("Пирог", 3.99, "Десерт"))
        summary = order.get_order_summary()
        self.assertIn("Заказ для стола 2", summary)
        self.assertIn("Чай: 1.99₽", summary)
        self.assertIn("Пирог: 3.99₽", summary)
        self.assertIn("Итого: 5.98₽", summary)

    def test_book_table(self):
        """Тест бронирования столика"""
        booking = self.rm.book_table("Иван", 5, "19:00")
        self.assertEqual(booking['customer'], "Иван")
        self.assertEqual(booking['table'], 5)
        self.assertEqual(len(self.rm.bookings), 1)

    def test_get_menu_list(self):
        """Тест получения списка меню"""
        menu_list = self.rm.get_menu_list()
        self.assertEqual(len(menu_list), 2)
        self.assertIn("Пицца", menu_list[0])
        self.assertIn("Салат", menu_list[1])


if __name__ == "__main__":
    unittest.main()