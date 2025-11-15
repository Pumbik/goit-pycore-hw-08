from models import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Error: Contact not found."

    return inner



@input_error
def add_birthday(args, book):
    name, birthday_date = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday_date)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday is on {record.birthday}."
        else:
            return f"No birthday information for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next 7 days."
    
    result_lines = ["Upcoming birthdays in the next 7 days:"]
    for entry in upcoming:
        result_lines.append(f"{entry['name']} - Congratulate on: {entry['congratulation_date']}")
    
    return "\n".join(result_lines)

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(phone.value for phone in record.phones)
        return f"{name}'s phone numbers: {phones}"
    else:
        return f"Contact {name} not found."

@input_error
def show_all_contacts(book: AddressBook):
    if not book.data:
        return "No contacts in the address book."
    result_lines = []
    for record in book.data.values():
        result_lines.append(str(record))
    return "\n".join(result_lines)
