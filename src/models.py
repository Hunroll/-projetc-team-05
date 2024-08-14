from datetime import datetime
from os import remove
from typing import Any, List
import re
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
        self.__value = None
        super().__init__(value)


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        self.__value = normalize_phone(phone)



class Birthday(Field):
    """Class for representing a birthday field.
    __init__:
        value: str
            The birthday of the contact in format DD.MM.YYYY
    __errors_handling__:
        ValueError: if the date does not match the format or is a future date
    """
    def __init__(self, value: str):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if value > datetime.now():
            raise ValueError("Birthday can\'t be a future date")
        self.__value = value

    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

class Email(Field):
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        # Регулярний вираз для перевірки електронної пошти
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(regex, value):
            raise ValueError("Incorrect email format")


class Address(Field):
    def __init__(self, value):
        super().__init__(value)
        
class UserRecord:
    """Class for representing a contact record.
    __init__:
        name: str (required)
            The name of the contact
        Optional arguments (all private):
        phones: List[str]
            The phone numbers of the contact. Valid format '0XXXXXXXXX' or '+380XXXXXXXXX'
        birthday: str
            The birthday of the contact. Valid format DD.MM.YYYY
        emails: List[str]
            The email addresses of the contact. Valid format string user@subdomain.domain
        address: str
            The address of the contact. Without any validation.
        """
    def __init__(self, name: str,
                 phones: List[str]=None,
                 birthday: str=None,
                 emails: List[str]=None,
                 address: str=None):
        self.name = Name(name)
        self.__phones = []
        self.__birthday = None
        self.__address = None
        self.__emails = []

        if phones:
            self.phones = phones

        if birthday:
            self.birthday = birthday

        if emails:
            self.emails = emails

        if address:
            self.address = address

        if emails:
            self.emails = emails

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"\nbirthday: {self.birthday if self.birthday else 'Not set'}, "
                f"\nphones: {'; '.join(self.phones)}, "
                f"\nemail: {'; '.join(self.emails)}, "
                f"\naddress: {self.address if self.address else 'Not set'}")

    @property
    def phones(self):
        return (p.value for p in self.__phones)

    @phones.setter
    def phones(self, phones: List[str]):
        for phone in phones:
            self.add_phone(phone)

    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone not in self.__phones:
            self.__phones.append(phone)
        else:
            raise ValueError(f"[ERROR] Number {phone} already exists in the record {self.name.value}")

    @phones.setter
    def phones(self, phones: List[str]):
        for phone in phones:
            self.add_phone(phone)

    def remove_phone(self, phone: str):
        phone = Phone(phone)
        if phone not in self.__phones:
            raise ValueError(f"{phone.value} does not exist")
        else:
            self.__phones.remove(phone)

    def edit_phone(self, phone: str, new_phone: str):
        if Phone(phone) not in self.__phones:
            raise ValueError(f"{phone} does not exist")
        self.add_phone(new_phone)  # Try to add new phone raises an error if the phone already exists
        self.remove_phone(phone)   # Remove the old phone if the new one was added successfully. Otherwise, the old phone remains in the list

    def find_phone(self, phone: Phone) -> Phone|None:
        return phone if phone in self.phones else None

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: str):
        birthday = Birthday(birthday)
        self.__birthday = birthday

    @property
    def emails(self):
        return self.__emails

    @emails.setter
    def emails(self, emails: List[str]):
        for email in emails:
            self.add_email(email)

    def add_email(self, email):
        self.__emails.append(Email(email))

    def remove_email(self, email):
        email = Email(email)
        if email not in self.__emails:
            raise ValueError(f"{email.value} does not exist")
        else:
            self.__emails.remove(email)

    def edit_email(self, email, new_email):
        if Email(email) not in self.__emails:
            raise ValueError(f"{email} does not exist")
        self.add_email(new_email)
        self.remove_email(email)

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        address_inst = Address(address)
        self.__address = address_inst
