from collections import UserDict
from datetime import datetime, timedelta

# Classes for Fields, Record, and AddressBook

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Невірни формат телефону. Телефон повинен містити 10 цифр.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # 1. Перетворюємо рядок на об'єкт datetime
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            # 2. Зберігаємо саме об'єкт datetime, а не рядок
            super().__init__(parsed_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return

    def edit_phone(self, old_phone, new_phone):
        # отримаємо одразу індекс
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                #валідуємо новий номер
                valid_new_phone = Phone(new_phone)
                self.phones[i] = valid_new_phone
                return  
    
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_date):
        self.birthday = Birthday(birthday_date)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name] 

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value.date()
                # Визначаємо дату дня народження цього року
                birthday_this_year = birthday.replace(year=today.year)
                #  Перевіряємо, чи день народження вже минув
                if birthday_this_year < today:
                    # Розглядаємо дату наступного року
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                # Розраховуємо різницю в днях
                delta_days = (birthday_this_year - today).days
                
                # Перевіряємо, чи потрапляє у наш 7-денний проміжок
                if 0 <= delta_days < 7:
                    congratulation_date = birthday_this_year
                    
                    # Перевіряємо, чи це вихідний
                    if congratulation_date.weekday() >= 5: # 5=Субота, 6=Неділя
                        # Якщо так, переносимо на понеділок
                        days_to_add = 7 - congratulation_date.weekday()
                        congratulation_date += timedelta(days=days_to_add)
                    
                    # Додаємо результат
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
                
        return upcoming_birthdays