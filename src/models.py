import re
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return other.__class__ == self.__class__ and other.value == self.value
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if (not re.match(r'^\d{10,10}$', value)):
            raise ValueError("Incorrect phone number")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if value > datetime.now():
            raise ValueError("Birthday can\'t be a future date")
        self.value = value
    
    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

class Email(Field):
    def __init__(self, value):
        # Регулярний вираз для перевірки електронної пошти
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(regex, value):
            raise ValueError("Incorrect email format")
        super().__init__(value)

class Address(Field):
    def __init__(self, value):
        super().__init__(value)
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.__phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday if self.birthday else 'Not set'}, phones: {'; '.join(self.phones)}, email: {self.email if self.email else 'Not set'}, address: {self.address if self.address else 'Not set'}"
    
    def add_phone(self, phone):
        phone = Phone(phone)
        if phone not in self.__phones:
            self.__phones.append(phone)
        else:
            raise ValueError("This number already exists")

    def remove_phone(self, phone):
        phone = Phone(phone)
        self.__phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        phone = Phone(phone)
        new_phone = Phone(new_phone)
        if phone not in self.__phones:
            raise ValueError(f"{phone.value} does not exist")
        if new_phone in self.__phones:
            raise ValueError(f"{new_phone.value} already exists")
        self.__phones = list(map(lambda p: p if p != phone else new_phone, self.__phones))


    @property
    def phones(self):
        return (p.value for p in self.__phones)
        

    def find_phone(self, phone) -> Phone:
        return phone if phone in self.phones else None

    def add_birthday(self, birthday):
        birthday = Birthday(birthday)
        self.birthday = birthday

    def add_email(self, email):
        email = Email(email)
        self.email = email

    def add_address(self, address):
        address = Address(address)
        self.address = address
