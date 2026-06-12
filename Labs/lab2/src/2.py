class Train:
    def __init__(self, train_data):
        self.number = train_data["number"]

        self.destination = train_data["destination"]

        self.date = train_data["date"]

        self.time = train_data["time"]

        self.price = train_data["price"]

    def __str__(self):
        return (
            f"Поезд: {self.number} | "
            f"Станция: {self.destination} | "
            f"Дата: {self.date} | "
            f"Время: {self.time} | "
            f"Цена: {self.price}"
        )


class TicketSystem:
    def __init__(self):
        self.trains = []

    def add_train(self):
        number = input("Номер поезда: ")
        destination = input("Станция назначения: ")
        date = input("Дата поездки: ")
        time = input("Время поездки: ")
        price = float(input("Цена билета: "))

        train_data = {
            "number": number,
            "destination": destination,
            "date": date,
            "time": time,
            "price": price,
        }

        train = Train(train_data)

        self.trains.append(train)

        print("Поезд добавлен")

    def find_trains(self):
        destination = input("Введите станцию: ")
        date = input("Введите дату: ")
        time = input("Введите время: ")

        found = []

        for train in self.trains:
            if train.destination.lower() == destination.lower() and train.date == date and train.time == time:
                found.append(train)

        if not found:
            print("Подходящих поездов нет")
            return

        print("\nНайденные поезда:")

        for index, train in enumerate(found, start=1):
            print(f"{index}. {train}")

        choice = int(input("Выберите поезд: ")) - 1

        if 0 <= choice < len(found):
            selected = found[choice]

            print("\nСчет на оплату")
            print(selected)
            print(f"К оплате: {selected.price}")

        else:
            print("Неверный выбор")

    def show_trains(self):
        if not self.trains:
            print("Список поездов пуст")
            return

        for train in self.trains:
            print(train)


system = TicketSystem()

while True:
    print("\n1 - Добавить поезд")
    print("2 - Найти поезд")
    print("3 - Показать поезда")
    print("0 - Выход")

    command = input("Выберите действие: ")

    if command == "1":
        system.add_train()

    elif command == "2":
        system.find_trains()

    elif command == "3":
        system.show_trains()

    elif command == "0":
        break

    else:
        print("Неверная команда")
