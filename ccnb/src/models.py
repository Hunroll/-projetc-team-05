from datetime import datetime
from typing import Any, List

from prompt_toolkit.completion import Completer, Completion

from ccnb.src.Validator import Validator


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
    use Validator to normalize and validate phone number
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
        self.__value = Validator.normalize_phone(phone)



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
        self.__value = Validator.validate_birthday(value)

    def __str__(self):
        return datetime.strftime(self.value, "%d.%m.%Y")

class Email(Field):
    """Class for representing an email field with validation.
    valid email format:
    1) all characters before '@' are alphanumeric, '.' or '_'
    2) '@' is present
    3) all characters after '@' are alphanumeric or '.'
    4) '.' is present
    5) the domain part contains only letters
    """
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = Validator.validate_email(value)


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
        self.__name = Name(name)  # For make sure that the name is always a Name instance
        self.__phones = []        # For validation and normalization
        self.__birthday = None    # For validation and formatting
        self.__emails = []        # For validation
        self.__address = None     # For make sure that the address is always an Address instance + prepare for future validation

        if phones:
            self.phones = phones

        if birthday:
            self.birthday = birthday

        if emails:
            self.emails = emails

        if address:
            self.address = address

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"\nbirthday: {self.birthday if self.birthday else 'Not set'}, "
                f"\nphones: {'; '.join(self.phones) if self.phones else 'Not set'}, "
                f"\nemail: {'; '.join(self.emails) if self.emails else 'Not set'}, "
                f"\naddress: {self.address if self.address else 'Not set'}")

    @staticmethod
    def truncate_list_of_recs(records) -> str:
        records = list(records) if records else None
        if records is None or len(records) == 0:
            return 'Not set'
        if len(records) ==1:
            return records[0]
        if len(records) > 1:
            return records[0] + "; ..."

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = Name(name)

    @property
    def phones(self):
        if len(self.__phones) == 0:
            return None
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
        if len(self.__emails) == 0:
            return None
        return (email.value for email in self.__emails)

    @emails.setter
    def emails(self, emails: List[str]):
        for email in emails:
            self.add_email(email)

    def add_email(self, email):
        email = Email(email)
        if email not in self.__emails:
            self.__emails.append(email)
        else:
            raise ValueError(f"[ERROR] Email {email} already exists in the record {self.name.value}")

    def remove_email(self, email):
        email = Email(email)
        if email not in self.__emails:
            raise ValueError(f"{email.value} does not exist")
        else:
            self.__emails.remove(email)

    def edit_email(self, email, new_email):
        if Email(email) not in self.__emails:
            raise ValueError(f"{email} does not exist")
        self.add_email(new_email)  # Try to add new email raises an error if the email already exists
        self.remove_email(email)   # Remove the old email if the new one was added successfully. Otherwise, the old email remains in the list

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        address_inst = Address(address)
        self.__address = address_inst

class Title(Field):
    """Class for representing the title of a note."""
    pass

class Content(Field):
    """Class for representing the content of a note."""
    def short_string(self, length = 40):
        full_str = str(self)
        return full_str if len(full_str) <= 40 else (full_str[0:length - 4] + "...")
    pass

class Tags(Field):
    """Class for representing tags of a note. Contains a list of strings"""
    def __init__(self, value: List[str]):
        super().__init__(value)

class Note:
    """Class for representing a note with title, content, and tags.
    __init__:
        title: str
            The title of the note
        content: str
            The content of the note
        tags: List[str]
            The tags of the note
    Methods:
        add_tag(tag: str)
            Adds a tag to the note if it does not already exist
        remove_tag(tag: str)
            Removes a tag from the note if it exists
        edit_content(new_content: str)
            Updates the content of the note
        search_by_keyword(keyword: str) -> bool
            Searches for a keyword in the title, content, and tags of the note
    """
    def __init__(self, title: str, content: str, tags: List[str] = None):
        self.title = Title(title)
        self.content = Content(content)
        self.tags = Tags(tags) if tags else Tags([])

    def __str__(self):
        tags_str = ', '.join(self.tags.value) if self.tags.value else 'No tags'
        return f"Title: {self.title.value}\nContent: {self.content.value}\nTags: {tags_str}"

    def add_tag(self, tag: str):
        if tag not in self.tags.value:
            self.tags.value.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.tags.value:
            self.tags.value.remove(tag)

    def edit_content(self, new_content: str):
        self.content = Content(new_content)

    def search_by_keyword(self, keyword: str) -> bool:
        keyword = keyword.lower()
        return keyword in self.title.value.lower() or keyword in self.content.value.lower() or any(keyword in tag.lower() for tag in self.tags.value)


class CustomCommandCompleter(Completer):
    """Custom class to detect first word in command line and give suggestions"""
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        # Get text before cursor
        text = document.text_before_cursor

        # If space in string - skip
        if ' ' in text:
            return

        # Works as usual
        for cmd in self.commands:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))
