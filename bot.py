from address_book import AddressBook, Record
from datetime import datetime, timedelta
import random
import sys


class TooManyArgsError(Exception):
    pass


class ContactAbsentError(Exception):
    pass


class ContactPresentError(Exception):
    pass


class ContactListEmptyError(Exception):
    pass


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Insufficient parameters, please try again."
        except ValueError:
            return "Entered data is not valid."
        except TooManyArgsError:
            return "Too many parameters, please try again."
        except ContactAbsentError:
            return "Contact is not found, use \"add\" command to add it."
        except ContactPresentError:
            return "Contact is already present, use \"change\" command to overwrite the phone."
        except ContactListEmptyError:
            return "Contacts list is empty."

    return inner


@input_error
def add_contact(args, book: AddressBook):
    if len(args) > 2:
        raise TooManyArgsError

    name = args[0]
    phone = args[1]

    if book.find(name):
        raise ContactPresentError

    record = Record(name)
    record.add_phone(phone)

    book.add_record(record)

    return "Contact added."


@input_error
def change_contact(args, book: AddressBook):
    if len(args) > 2:
        raise TooManyArgsError

    name = args[0]
    phone = args[1]

    record = book.find(name)

    if not record:
        raise ContactAbsentError

    record.edit_phone(record.phones[0].value, phone)

    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) > 1:
        raise TooManyArgsError

    name = args[0]

    record = book.find(name)

    if not record:
        raise ContactAbsentError

    return record.phones[0]


@input_error
def show_all(book: AddressBook):
    if len(book.data) == 0:
        raise ContactListEmptyError

    rows = []

    for name, record in book.data.items():
        rows.append(str(record))

    return '\n'.join(rows)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) > 2:
        raise TooManyArgsError

    name = args[0]
    birthday = args[1]

    record = book.find(name)

    if not record:
        raise ContactAbsentError

    record.add_birthday(birthday)

    return "Contact updated."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) > 1:
        raise TooManyArgsError

    name = args[0]

    record = book.find(name)

    if not record:
        raise ContactAbsentError

    return str(record.birthday) if record.birthday else 'Birthday not set'


@input_error
def birthdays(book: AddressBook):
    rows = []
    for day, records in book.birthdays():
        rows.append(day)

        for record in records:
            rows.append(str(record))

        rows.append('')

    return '\n'.join(rows)


def main():
    book = AddressBook()

    if (len(sys.argv) > 1 and sys.argv[1] == 'demo'):
        fill_demo_data(book)

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        if not user_input:
            print("No command entered.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


def fill_demo_data(book):
    contacts = [
        ('Alex', '1234567890'),
        ('Andy', '0987654321'),
        ('John smith', '1111111111'),
        ('John Doe', '2222222222'),
        ('Jane Doe', '3333333333'),
    ]

    delimiter = '-'*20

    for name, phone in contacts:
        birthday = datetime.today().replace(year=random.randint(1980, 2000)) + \
            timedelta(days=random.randint(1, 7))

        print(f"Adding {name}:")

        print(add_contact((name, phone), book))
        print(add_birthday((name, birthday.strftime('%d.%m.%Y')), book))
        print(show_phone((name,), book))
        print(show_birthday((name,), book))
        print()

    print('Birthdays:')
    print(birthdays(book))
    print(delimiter)
    print('Show all:')
    print(show_all(book))
    print(delimiter)

    name = contacts[0][0]
    phone = '9999999999'
    birthday = '01.11.2001'

    print(f'Changing {name} phone and birthday to: {phone} {birthday}')
    print(change_contact((name, phone), book))
    print(add_birthday((name, birthday), book))
    print(delimiter)
    print(show_all(book))
    print(delimiter)

    print('Supplying wrong data:')
    print(add_contact(tuple(), book))
    print(add_contact(('AAA',), book))
    print(add_contact(('AAA', phone, birthday), book))
    print(change_contact(('AAA',), book))
    print(change_contact((name,), book))
    print(change_contact((name, 'wrong phone'), book))
    print(add_birthday((name, 'wrong birthday'), book))
    print(delimiter)


if __name__ == "__main__":
    main()
