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

    def test_add_duplicate_menu_item(self):
        """Тест добавления дубликата блюда"""
        with self.assertRaises(ValueError):
            self.rm.add_menu_item("Пицца", 15.99, "Основное")

    def test_remove_menu_item(self):
        """Тест удаления блюда из меню"""
        result = self.rm.remove_menu_item("Пицца")
        self.assertTrue(result)
        self.assertEqual(len(self.rm.menu), 1)

    def test_remove_nonexistent_item(self):
        """Тест удаления несуществующего блюда"""
        result = self.rm.remove_menu_item("Бургер")
        self.assertFalse(result)

    def test_edit_menu_item_price(self):
        """Тест изменения цены блюда"""
        result = self.rm.edit_menu_item_price("Пицца", 15.99)
        self.assertTrue(result)
        self.assertEqual(self.rm.menu[0].price, 15.99)

    def test_menu_item_info(self):
        """Тест получения информации о блюде"""
        item = MenuItem("Паста", 10.99, "Паста")
        self.assertEqual(item.get_info(), "Паста (Паста) - 10.99₽")

    def test_create_order(self):
        """Тест создания заказа"""
        order = self.rm.create_order(3)
        self.assertEqual(order.table_number, 3)
        self.assertEqual(len(self.rm.orders), 1)

    def test_create_order_invalid_table(self):
        """Тест создания заказа с неверным номером стола"""
        with self.assertRaises(ValueError):
            self.rm.create_order(0)
        with self.assertRaises(ValueError):
            self.rm.create_order(-5)

    def test_add_item_to_order(self):
        """Тест добавления блюда в заказ"""
        order = Order(1)
        menu_item = MenuItem("Кофе", 2.99, "Напиток")
        order.add_item(menu_item)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.total, 2.99)

    def test_remove_item_from_order(self):
        """Тест удаления блюда из заказа"""
        order = Order(1)
        order.add_item(MenuItem("Кофе", 2.99, "Напиток"))
        order.add_item(MenuItem("Чай", 1.99, "Напиток"))
        order.remove_item(0)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(round(order.total, 2), 1.99)

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

    def test_empty_order_summary(self):
        """Тест сводки пустого заказа"""
        order = Order(1)
        summary = order.get_order_summary()
        self.assertIn("нет позиций", summary)

    def test_book_table(self):
        """Тест бронирования столика"""
        booking = self.rm.book_table("Иван", 5, "19:00")
        self.assertEqual(booking['customer'], "Иван")
        self.assertEqual(booking['table'], 5)
        self.assertEqual(booking['status'], "active")
        self.assertEqual(len(self.rm.bookings), 1)

    def test_book_table_invalid_data(self):
        """Тест бронирования с неверными данными"""
        with self.assertRaises(ValueError):
            self.rm.book_table("", 5, "19:00")
        with self.assertRaises(ValueError):
            self.rm.book_table("Иван", 0, "19:00")
        with self.assertRaises(ValueError):
            self.rm.book_table("Иван", 5, "")

    def test_cancel_booking(self):
        """Тест отмены бронирования"""
        self.rm.book_table("Иван", 5, "19:00")
        result = self.rm.cancel_booking("Иван", 5, "19:00")
        self.assertTrue(result)

        active = self.rm.get_active_bookings()
        self.assertEqual(len(active), 0)

    def test_cancel_nonexistent_booking(self):
        """Тест отмены несуществующего бронирования"""
        result = self.rm.cancel_booking("Петр", 10, "20:00")
        self.assertFalse(result)

    def test_get_active_bookings(self):
        """Тест получения активных бронирований"""
        self.rm.book_table("Иван", 5, "19:00")
        self.rm.book_table("Мария", 3, "20:00")
        self.rm.cancel_booking("Иван", 5, "19:00")

        active = self.rm.get_active_bookings()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]['customer'], "Мария")

    def test_get_menu_list(self):
        """Тест получения списка меню"""
        menu_list = self.rm.get_menu_list()
        self.assertEqual(len(menu_list), 2)
        self.assertIn("Пицца", menu_list[0])
        self.assertIn("Салат", menu_list[1])

    def test_get_total_revenue(self):
        """Тест подсчета выручки"""
        order = self.rm.create_order(1)
        order.add_item(MenuItem("Пицца", 12.99, "Основное"))
        self.assertEqual(self.rm.get_total_revenue(), 12.99)


if __name__ == "__main__":
    unittest.main()
