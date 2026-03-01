#!/usr/bin/env python3

import re

def is_valid_phone(phone: str) -> bool:
    pattern = r'^(\+\d{1,3})?\d{10}$|^\+380\d{9}$'
    return bool(re.match(pattern, phone.replace('-', '').replace(' ', '')))

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Введіть, будь ласка, ім'я та номер телефону у форматі +380XXXXXXXXX або 10 цифр."
        except IndexError:
            return "Недостатньо аргументів."
        except KeyError:
            return "Контакт не знайдено."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    if not is_valid_phone(phone):
        raise ValueError()
    contacts[name] = phone
    return "Контакт додано."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if not is_valid_phone(phone):
        raise ValueError()
    contacts[name] = phone
    return "Контакт оновлено."

@input_error
def show_phone(args, contacts):
    name = args[0]
    return f"{name} має номер {contacts[name]}"

@input_error
def show_all_contacts(contacts):
    if contacts:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
    else:
        return "Контактів не знайдено."

def main():
    contacts = {}
    print("Ласкаво просимо до бота-помічника!")

    commands = {
        "add": lambda args: add_contact(args, contacts),
        "change": lambda args: change_contact(args, contacts),
        "phone": lambda args: show_phone(args, contacts),
        "all": lambda args: show_all_contacts(contacts),
        "hello": lambda args: "Чим я можу вам допомогти?"
    }

    while True:
        user_input = input("Введіть команду: ")

        if not user_input.strip():
            print("Доступні команди: add, change, phone, all, hello, close, exit.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break
        if command in commands:
            print(commands[command](args))
        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()