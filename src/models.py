from datetime import datetime
from typing import Any, List

from src.normalize_phone import normalize_phone


class Field:
    """Base class for representing fields with a value."""
    def __init__(self, value: Any):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return other.__class__ == self.__class__ and other.value == self.value
    
class Name(Field):
    """Class for representing a name field."""
    pass

class Phone(Field):
    """Class for representing a phone field.
    use normalize_phone function to normalize and validate phone number
    __init__:
        phone: str
            The phone number of the contact in format '0XXXXXXXXX' or '+380XXXXXXXXX'
    __errors_handling__:
        ValueError: if the phone number does not match any of the known formats.
    """
    def __init__(self, value: str):
        super().__init__(normalize_phone(value))

class Birthday(Field):
    """Class for representing a birthday field.
    __init__:
        value: str
            The birthday of the contact in format DD.MM.YYYY
    __errors_handling__:
        ValueError: if the date does not match the format or is a future date
    """
    def __init__(self, value: str):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if value > datetime.now():
            raise ValueError("Birthday can\'t be a future date")
        super().__init__(value)
    
    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

        
class Record:
    """Class for representing a contact record.
    __init__:
        name: str
            The name of the contact
        """
    def __init__(self, name: str, phones: List[str]=None, birthday: str=None):
        self.name = Name(name)
        if phones is None:
            phones = []
        else:
            phones = [Phone(p) for p in phones]
        self.__phones = phones
        if birthday:
            self.add_birthday(birthday)
        else:
            self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, \nbirthday: {self.birthday if self.birthday else 'Not set'}, \nphones: {'; '.join(self.phones)}"
    
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone not in self.__phones:
            self.__phones.append(phone)
        else:
            raise ValueError(f"[ERROR] Number {phone} already exists in the record {self.name.value}")

    def remove_phone(self, phone: str):
        phone = Phone(phone)
        self.__phones.remove(phone)

    def edit_phone(self, phone: str, new_phone: str):
        phone = Phone(phone)
        new_phone = Phone(new_phone)
        if phone not in self.__phones:
            raise ValueError(f"{phone.value} does not exist")
        elif new_phone in self.__phones:
            raise ValueError(f"{new_phone.value} already exists")
        else:
            self.__phones = list(map(lambda p: p if p != phone else new_phone, self.__phones))

    @property
    def phones(self):
        return (p.value for p in self.__phones)
        

    def find_phone(self, phone: Phone) -> Phone|None:
        return phone if phone in self.phones else None

    def add_birthday(self, birthday: str):
        birthday = Birthday(birthday)
        self.birthday = birthday
