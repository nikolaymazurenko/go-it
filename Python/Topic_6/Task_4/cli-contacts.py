#!/usr/bin/env python3

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args) != 2:
        return "Помилка: команда 'add' вимагає два аргументи - ім'я та номер телефону."
    name, phone = args
    contacts[name] = phone
    return "Контакт додано."

def change_contact(args, contacts):
    if len(args) != 2:
        return "Помилка: команда 'change' вимагає два аргументи - ім'я та новий номер телефону."
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Контакт оновлено."
    else:
        return "Контакт не знайдено."

def show_phone(args, contacts):
    if len(args) != 1:
        return "Помилка: команда 'phone' вимагає один аргумент - ім'я контакту."
    name = args[0]
    if name in contacts:
        return f"{name} має номер {contacts[name]}"
    else:
        return "Контакт не знайдено."

def show_all_contacts(contacts):
    if contacts:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
    else:
        return "Контактів не знайдено."

def main():
    contacts = {}
    print("Ласкаво просимо до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        if len(user_input.strip()) == 0:
            print("Доступні команди: add, change, phone, all, hello, close, exit.")
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим я можу вам допомогти?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all_contacts(contacts))
        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
