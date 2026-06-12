class RemoveVowels:
    def encrypt(self, source_text):
        vowels = "аеёиоуыэюяaeiouAEIOUАЕЁИОУЫЭЮЯ"

        return "".join(char for char in source_text if char not in vowels)


class CaesarCipher:
    def __init__(self, shift_value):
        self.shift_value = shift_value

    def encrypt(self, source_text):
        encrypted_text = ""

        for char in source_text:
            encrypted_text += chr(ord(char) + self.shift_value)

        return encrypted_text


class Encryptor:
    def __init__(self, strategy):
        self.strategy = strategy

    def encrypt(self, source_text):
        return self.strategy.encrypt(source_text)


file_name = input("Введите имя txt файла: ")

with open(
    file_name,
    "r",
    encoding="utf-8",
) as file:
    file_text = file.read()

print("1 - Удалить гласные")

print("2 - Шифр Цезаря")

choice = input("Выберите метод: ")

if choice == "1":
    encryptor = Encryptor(RemoveVowels())

    result_text = encryptor.encrypt(file_text)

    with open(
        "no_vowels.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(result_text)

    print("Результат сохранен в no_vowels.txt")

elif choice == "2":
    shift_number = int(input("Введите сдвиг: "))

    encryptor = Encryptor(CaesarCipher(shift_number))

    result_text = encryptor.encrypt(file_text)

    with open(
        "encrypted.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(result_text)

    print("Результат сохранен в encrypted.txt")

else:
    print("Неверный выбор")
