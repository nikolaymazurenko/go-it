#!/usr/bin/env python3

from collections import UserDict
from datetime import datetime, timedelta



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
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр.")
        self.__value = value


class Birthday(Field):
    def __init__(self, value):
        self.value = value  # triggers property setter

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d.%m.%Y")
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
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", день народження: {self.birthday}" if self.birthday else ""
        return f"Ім'я контакту: {self.name.value}, телефони: {phones_str}{birthday_str}"


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
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        msg = "Контакт додано."
    else:
        msg = "Контакт оновлено."
    record.add_phone(phone)
    return msg

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.edit_phone(old_phone, new_phone):
        raise ValueError(f"Телефон {old_phone} не знайдено.")
    return "Контакт оновлено."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return "; ".join(p.value for p in record.phones)

@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Адресна книга порожня."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "День народження додано."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"У контакту {name} немає дня народження."
    return str(record.birthday)

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Найближчого тижня днів народження немає."
    return "\n".join(f"{item['name']}: {item['birthday']}" for item in upcoming)

def hello():
    return "Чим я можу вам допомогти?"

def parse_input(user_input: str):
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, *args

def main():
    book = AddressBook()
    print("Ласкаво просимо до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print(hello())

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
