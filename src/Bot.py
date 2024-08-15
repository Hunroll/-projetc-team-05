import re
from datetime import datetime, timedelta
from colorama import Fore, Style
from src.AddressBook import AddressBook
from src.data_base import DataBase
from src.models import *
from src.NoteBook import NoteBook
import functools # Metadata import from function into decorator

CMD_EXIT="exit"
CMD_NA="n/a"
class Bot:
    current_user: str
    address_book: AddressBook
    note_book: NoteBook

    def __init__(self, user_name: str): 
        self.__current_user = user_name.lower() # TODO: Normalize and validate user_name
        database = DataBase.load_data(self.current_user)
        self.address_book = database.address_book
        self.note_book = database.note_book
    

    @property
    def current_user(self):
        return self.__current_user

    @current_user.setter
    def current_user(self, user_name):
        # TODO: Validation of user_name place here
        pass

    @staticmethod
    def input_error(func):
        @functools.wraps(func) # Get oiginal metadata from functions
        def inner(*args, **kwargs) -> str:
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                return Fore.RED + "; ".join(e.args)
            except IndexError as e:
                return Fore.RED + "; ".join(e.args)
            except KeyError as e:
                return Fore.YELLOW + "; ".join(e.args)
        return inner

    @staticmethod
    #returns command key and args if any
    def parse_input(inp: str) -> tuple[str, tuple]:
        cmd, *args = inp.split()
        cmd = cmd.lower()
        return cmd, *args

    @input_error
    def say_hello(self, *args) -> str:
        '''hello, Greet the bot.'''
        if len(*args):
            raise IndexError("\"hello\" doesn\'t need arguments")
        return f"How can I help you, {self.current_user}?"

    @input_error
    def finalize(self, *args) -> str:
        '''exit || close, Exit the bot.'''
        DataBase.save_data(self.address_book, self.note_book, self.current_user)
        return "DB is saved. Good bye!"

    @input_error
    def add_contact(self, *args) -> str:
        '''add [name] [phone], Add a new contact.'''
        if len(*args) != 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add _name_ _phone_\"")
        name, phone, *_ = args[0]
        mess = "Contact already exist. Just updated with new phone."
        contact = self.address_book.find(name)
        if not contact:
            self.address_book.add_record(UserRecord(name))
            contact = self.address_book.find(name)
            mess = "Contact added."
        contact.add_phone(phone)
        return mess

    @input_error
    def change_contact(self, *args) -> str:
        '''change [name] [phone], Change an existing contact's phone.'''
        # TODO: Try to use argparse module for parsing arguments
        # TODO: Add change_phone, change_email, change_address methods
        if len(*args) != 3:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"change _name_ _old_phone_ _new_phone_\"")
        name, old_phone, new_phone, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist, please use \"add {name} {new_phone}\"")

        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def get_phone(self, *args) -> str:
        '''phone [name], Show the phone number of the contact.'''
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"phone _name_ \"")
        name, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str.join("; ", contact.phones)

    @input_error
    def search_contact(self, *args) -> str:
        '''search [arg], Search contact.'''
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"search _name_ \"")
        pattern, *_ = args[0]

        return str.join("\n", [str(contact) for contact in self.address_book.search(pattern)])

    @input_error
    def get_all(self, *args) -> str:
        '''all, Show all contacts.'''
        if len(*args):
            raise IndexError("\"all\" doesn\'t need arguments")
        if len(self.address_book) == 0:
            return "It\'s lonely here:( Please use \"add\" command"
        result_str = "{:<20} {:<12} {:<20} {:<20} {:<20}\n".format("Name", "Birthday", "Phone(s)", "Email(s)", "Address")
        for k, user in self.address_book.items():
            result_str += "{:<20} {:<12} {:<20} {:<20} {:<20}\n".format(
                str(user.name), 
                str(user.birthday) if user.birthday else 'Not set', 
                '; '.join(user.phones),
                str(user.emails) if user.emails else 'Not set',
                str(user.address) if user.address else 'Not set' )
        return result_str

    @input_error
    def add_birthday(self, *args) -> str:
        '''add-birthday [name] [DD.MM.YYYY], Add birthday to existing contact.'''
        if len(*args) != 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add-birthday _name_ _DD.MM.YYYY_\"")
        name, birthday, *_ = args[0]
        
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        
        contact.add_birthday(birthday)
        return "Contact updated."

    @input_error
    def show_birthday(self, *args) -> str:
        '''show-birthday [name], Show the birthday of an existing contact.'''
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"show-birthday _name_ \"")
        name, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str(contact.birthday) if contact.birthday else f"{name} doesn\'t have birthday set"

    @input_error
    def birthdays(self, *args) -> str:
        '''birthdays, Show upcoming birthdays.'''
        if len(*args):
            raise IndexError("\"birthdays\" doesn\'t need arguments")
        birth_dict = self.address_book.get_upcoming_birthdays()
        result_str = ""
        for bd in birth_dict:
            result_str += f"{str(bd['name']) : <20}{bd['congratulation_date'] : <20}\n"
        return result_str

    @input_error
    def add_email(self, *args) -> str:
        '''add-email [name] [email], Add email to existing contact.'''
        if len(*args) != 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add-email _name_ _email@example.com_\"")
        name, email, *_ = args[0]
        
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        
        contact.add_email(email)
        return "Contact updated."

    @input_error
    def add_address(self, *args) -> str:
        '''add-address [name] [address], Add address to existing contact.'''
        if len(*args) < 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add-address _name_ _address_\"")

        name = args[0][0]
        address = ' '.join(args[0][1:])
        
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        
        contact.address = address
        return "Contact updated."
    
    @input_error
    def delete_record(self, *args) -> str:
        '''delete-contact [name], Delete contact.'''
        """ Remove contact """
        name, *_ = args[0]
        self.address_book.delete(name)
        return f"Contact {name} removed."
    
    def add_note(self, args):
        '''add-note [title] [content], Add a new note.'''
        if len(args) < 2:
            return "Usage: add-note [title] [content]"
        title, content = args[0], " ".join(args[1:])
        return self.note_book.add_note(title, content)

    def edit_note(self, args):
        '''edit-note [title] [new_content], Edit an existing note.'''
        if len(args) < 2:
            return "Usage: edit-note [title] [new_content]"
        title, new_content = args[0], " ".join(args[1:])
        return self.note_book.edit_note(title, new_content)

    def delete_note(self, args):
        '''delete-note [title], Delete an existing note.'''
        if len(args) < 1:
            return "Usage: delete-note [title]"
        title = args[0]
        return self.note_book.delete_note(title)

    def search_notes(self, args):
        '''search-notes [keyword], Search for notes by keyword.'''
        if len(args) < 1:
            return "Usage: search-notes [keyword]"
        keyword = " ".join(args)
        return self.note_book.search_notes(keyword)

    def show_all_notes(self, args):
        '''show-notes, Show all notes.'''
        return self.note_book.show_all_notes()

    def register_handlers(self) -> dict:
        # If you added new function, update Help text in /main.py
        funcs = dict()
        funcs["hello"] = self.say_hello
        funcs["add"] = self.add_contact
        funcs["add-birthday"] = self.add_birthday
        funcs["change"] = self.change_contact
        funcs["phone"] = self.get_phone
        funcs["show-birthday"] = self.show_birthday
        funcs["all"] = self.get_all
        funcs["birthdays"] = self.birthdays
        funcs["add-email"] = self.add_email
        funcs["add-address"] = self.add_address
        funcs["search"] = self.search_contact
        funcs["add-note"]= self.add_note
        funcs["edit-note"]=self.edit_note
        funcs["delete-note"]=self.delete_note
        funcs["search-notes"]=self.search_notes
        funcs["show-notes"] = self.show_all_notes
        funcs["delete-contact"] = self.delete_record
        funcs["exit"] = funcs["close"] = self.finalize
        return funcs

    def print_handlers_list(self) ->list:
        ''' Handler's list for hello message '''
        handlers = self.register_handlers() # commands list
        command_descriptions = []
        seen_commands = set()

        # Get all functions descriptions
        for command, func in handlers.items():
            doc = func.__doc__ or "No description available."
            parts = doc.split(',', 1)
            if len(parts) == 2:
                name, description = parts
                name = name.strip()
                description = description.strip()
            else:
                name = doc.strip()
                description = "No description available."

            # Accepting only unique commands (exit || close could be 2 times in list)
            if name not in seen_commands:
                command_descriptions.append((name, description))
                seen_commands.add(name)
        
        # Nice list making
        max_len = max(len(cmd) for cmd, _ in command_descriptions)
        command_list = (
            f"{Fore.LIGHTGREEN_EX}\nAvailable commands:\n" +
            "".join(f"{Fore.LIGHTYELLOW_EX}- {cmd.ljust(max_len)}{Style.RESET_ALL} - {desc}\n" for cmd, desc in command_descriptions)
        )
        return command_list