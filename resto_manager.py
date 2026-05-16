# resto_manager.py
class MenuItem:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    
    def get_info(self):
        return f"{self.name} ({self.category}) - ${self.price}"

class Order:
    def __init__(self, table_number):
        self.table_number = table_number
        self.items = []
        self.total = 0
    
    def add_item(self, menu_item):
        self.items.append(menu_item)
        self.total += menu_item.price
    
    def get_order_summary(self):
        summary = f"Заказ для стола {self.table_number}:\n"
        for item in self.items:
            summary += f"  - {item.name}: ${item.price}\n"
        summary += f"Итого: ${self.total}"
        return summary

class RestaurantManager:
    def __init__(self):
        self.menu = []
        self.orders = []
        self.bookings = []
    
    def add_menu_item(self, name, price, category):
        item = MenuItem(name, price, category)
        self.menu.append(item)
        return item
    
    def create_order(self, table_number):
        order = Order(table_number)
        self.orders.append(order)
        return order
    
    def book_table(self, customer_name, table_number, time):
        booking = {
            'customer': customer_name,
            'table': table_number,
            'time': time
        }
        self.bookings.append(booking)
        return booking
    
    def get_menu_list(self):
        return [item.get_info() for item in self.menu]
    
    def get_total_revenue(self):
        total = sum(order.total for order in self.orders)
        return total

# Функция для демонстрации работы
def main():
    rm = RestaurantManager()
    
    # Добавляем блюда в меню
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

if __name__ == "__main__":
    main()