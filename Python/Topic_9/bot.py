#!/usr/bin/env python3

from collections import UserDict

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

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            self.phones.append(Phone(new_phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Ім'я контакту: {self.name.value}, телефони: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Контакт '{name}' видалено."
        else:
            return f"Контакт '{name}' не знайдено."


print("Створення нової адресної книги")
book = AddressBook()

print("Створення запису для John")
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

print("Додавання запису John до адресної книги")
book.add_record(john_record)

print("Створення запису для Jane")
jane_record = Record("Jane")
jane_record.add_phone("9876543210")

print("Додавання запису Jane до адресної книги")
book.add_record(jane_record)

print("Виведення всіх записів у книзі")
for name, record in book.data.items():
    print(record)

print("Знаходження та редагування телефону для John")
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print("Виведення оновленого запису John")
print(john) # Виведення: Contact name: John, phones: 1112223333; 5555555555

print("Пошук конкретного телефону в записі John")
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
print("Видалення запису Jane")