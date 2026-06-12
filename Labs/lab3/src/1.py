class Burger:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Drink:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.price for item in self.items)

    def show(self):
        for item in self.items:
            print(f"{item.name} - {item.price}")

        print(f"Итого: {self.total()}")


class Factory:
    @staticmethod
    def create_burger(choice):
        burgers = {
            "1": Burger("Chicken Burger", 300),
            "2": Burger("Vegan Burger", 250),
            "3": Burger("Cheese Burger", 350),
        }

        return burgers.get(choice)

    @staticmethod
    def create_drink(choice):
        drinks = {
            "1": Drink("Cola", 100),
            "2": Drink("Tea", 80),
            "3": Drink("Coffee", 120),
        }

        return drinks.get(choice)


order = Order()

print("Бургеры:")
print("1 - Chicken Burger")
print("2 - Vegan Burger")
print("3 - Cheese Burger")

burger_choice = input("Выберите бургер: ")

burger = Factory.create_burger(burger_choice)

if burger:
    order.add_item(burger)

print("\nНапитки:")
print("1 - Cola")
print("2 - Tea")
print("3 - Coffee")

drink_choice = input("Выберите напиток: ")

drink = Factory.create_drink(drink_choice)

if drink:
    order.add_item(drink)

print("\nВаш заказ:")
order.show()
