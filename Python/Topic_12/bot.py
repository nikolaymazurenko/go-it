#!/usr/bin/env python3

from collections import UserDict
from datetime import datetime, timedelta
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
        self.value = value  # triggers property setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр.")
        self._value = value


class Birthday(Field):
    def __init__(self, value):
        self.value = value  # triggers property setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте ДД.ММ.РРРР")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday_str = f", день народження: {self.birthday}" if self.birthday else ""
        return f"Ім'я контакту: {self.name.value}, телефони: {phones}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self, days_ahead=7):
        today = datetime.today().date()
        upcoming = []
        for user in self.data.values():
            if not user.birthday:
                continue
            bday = user.birthday.value.date()
            bday_this_year = bday.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)
            if today <= bday_this_year <= today + timedelta(days=days_ahead):
                upcoming.append(
                    {"name": user.name.value, "birthday": bday_this_year.strftime("%d.%m.%Y")}
                )
        return upcoming


class BotCommands:
    def __init__(self, book: AddressBook):
        self.book = book

    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                return str(e)
            except KeyError:
                return "Контакт не знайдено."
            except IndexError:
                return "Недостатньо аргументів."
        return inner

    @input_error
    def add_contact(self, args):
        if len(args) < 2:
            raise IndexError
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

    @input_error
    def show_phone(self, args):
        if len(args) < 1:
            raise IndexError
        record = self.book.find(args[0])
        if record is None:
            raise KeyError
        return "; ".join(p.value for p in record.phones)

    @input_error
    def show_all_contacts(self, args):
        if not self.book:
            return "Адресна книга порожня."
        return "\n".join(str(record) for record in self.book.values())

    @input_error
    def change_contact(self, args):
        if len(args) < 3:
            raise IndexError
        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record is None:
            raise KeyError
        if not record.edit_phone(old_phone, new_phone):
            return f"Телефон {old_phone} не знайдено."
        return "Контакт оновлено."

    @input_error
    def add_birthday(self, args):
        if len(args) < 2:
            return "Використання: add-birthday <name> <birthday>"
        name, birthday = args
        record = self.book.find(name)
        if record is None:
            return "Контакт не знайдено."
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            return str(e)
        return "День народження додано."

    @input_error
    def show_birthday(self, args):
        if len(args) < 1:
            raise IndexError
        name = args[0]
        record = self.book.find(name)
        if record is None:
            raise KeyError
        if record.birthday is None:
            return f"У контакту {name} немає дня народження."
        return str(record.birthday)

    @input_error
    def birthdays(self, args):
        upcoming = self.book.get_upcoming_birthdays()
        if not upcoming:
            return "Найближчого тижня днів народження немає."
        return "\n".join(f"{item['name']}: {item['birthday']}" for item in upcoming)

    @staticmethod
    def hello(args):
        return "Чим я можу вам допомогти?"

    @staticmethod
    def parse_input(user_input):
        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]
        return command, args


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
        "change": cmd.change_contact,
        "phone": cmd.show_phone,
        "all": cmd.show_all_contacts,
        "add-birthday": cmd.add_birthday,
        "show-birthday": cmd.show_birthday,
        "birthdays": cmd.birthdays,
        "hello": cmd.hello,
    }

    while True:
        user_input = input("Введіть команду: ")

        if not user_input.strip() or user_input in ["help", "?"]:
            print("Команди: add, change, phone, all, add-birthday, show-birthday, birthdays, hello, close, exit")
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
