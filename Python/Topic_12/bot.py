#!/usr/bin/env python3

from collections import UserDict
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return True
        return False

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            self.phones.append(Phone(new_phone))
            return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        return f"Ім'я контакту: {self.name.value}, телефони: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Контакт '{name}' видалено."
        return f"Контакт '{name}' не знайдено."


class BotCommands:
    def __init__(self, book: AddressBook):
        self.book = book

    def add_contact(self, args):
        if len(args) < 2:
            return "Використання: add <name> <phone>"

        name, phone = args[0], args[1]
        record = self.book.find(name)

        try:
            if record is None:
                record = Record(name)
                record.add_phone(phone)
                self.book.add_record(record)
            else:
                record.add_phone(phone)
        except ValueError as e:
            return str(e)

        return "Контакт додано."

    def show_phone(self, args):
        if not args:
            return "Вкажіть ім'я контакту."

        record = self.book.find(args[0])

        if record:
            return "; ".join(p.value for p in record.phones)

        return "Контакт не знайдено."

    def show_all_contacts(self, args):
        if not self.book:
            return "Адресна книга порожня."

        return "\n".join(str(record) for record in self.book.values())

    def change_contact(self, args):
        if len(args) < 3:
            return "Використання: change <name> <old_phone> <new_phone>"

        name, old_phone, new_phone = args
        record = self.book.find(name)

        if not record:
            return "Контакт не знайдено."

        try:
            if not record.edit_phone(old_phone, new_phone):
                return f"Телефон '{old_phone}' не знайдено у контакті '{name}'."
        except ValueError as e:
            return str(e)

        return "Телефон змінено."

    def delete_contact(self, args):
        if not args:
            return "Використання: delete <name>"
        return self.book.delete(args[0])

    @staticmethod
    def parse_input(user_input):
        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]
        return command, args

    @staticmethod
    def hello(args):
        return "Чим я можу вам допомогти?"



def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    cmd = BotCommands(book)

    commands = {
        "add": cmd.add_contact,
        "delete": cmd.delete_contact,
        "change": cmd.change_contact,
        "phone": cmd.show_phone,
        "all": cmd.show_all_contacts,
        "hello": cmd.hello,
    }

    while True:
        user_input = input("Введіть команду: ")

        if not user_input.strip() or user_input in ["help", "?"]:
            print("Команди: add, change, phone, all, delete, hello, close, exit")
            continue

        command, args = BotCommands.parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("До побачення!")
            break

        if command in commands:
            try:
                print(commands[command](args))
            except Exception as e:
                print(f"Помилка: {e}")
        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()