from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError

        self.value = value


class Birthday(Field):
    def __init__(self, value):
        if not re.match("^\d{2}\.\d{2}\.\d{4}$", value):
            raise ValueError

        self.value = value

    @property
    def date(self):
        return datetime.strptime(self.value, '%d.%m.%Y')


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        result = list(filter(lambda p: p.value == phone, self.phones))
        return result[0] if len(result) > 0 else None

    def remove_phone(self, phone):
        self.phones = list(filter(lambda p: p.value != phone, self.phones))

    def edit_phone(self, old_phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == old_phone:
                self.phones[i] = Phone(new_phone)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name)

    def birthdays(self):

        records_per_day = defaultdict(list)
        today = datetime.today().date()

        for name, record in self.data.items():
            birthday = record.birthday.date.date().replace(year=today.year)

            if birthday < today:
                birthday = birthday.replace(year=today.year+1)

            delta_days = (birthday - today).days

            if delta_days >= 7:
                continue

            weekday = birthday.weekday()

            if weekday >= 5:
                weekday = 0

            records_per_day[weekday].append(record)

        result = []

        for i in range(0, 7):
            check_day = today + timedelta(days=i)
            weekday = check_day.weekday()

            if weekday in records_per_day:
                result.append((check_day.strftime('%A'),
                              records_per_day[weekday]))

        return result


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("30.10.1987")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    print(book.birthdays())

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
