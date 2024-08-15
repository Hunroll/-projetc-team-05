import re
from datetime import datetime, timedelta
from colorama import Fore, Style
from src.AddressBook import AddressBook
from src.data_base import DataBase
from src.models import *
from src.NoteBook import NoteBook

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
        self.handlers = self.register_handlers()
        self.note_handlers = self.register_note_handlers()
    

    @property
    def current_user(self):
        return self.__current_user

    @current_user.setter
    def current_user(self, user_name):
        # TODO: Validation of user_name place here
        pass

    @staticmethod
    def input_error(func):
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
        if len(*args):
            raise IndexError("\"hello\" doesn\'t need arguments")
        return f"How can I help you, {self.current_user}?"

    @input_error
    def finalize(self, *args) -> str:
        DataBase.save_data(self.address_book, self.note_book, self.current_user)
        return "DB is saved. Good bye!"

    @input_error
    def add_contact(self, *args) -> str:
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
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"phone _name_ \"")
        name, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str.join("; ", contact.phones)

    @input_error
    def search_contact(self, *args) -> str:
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"search _name_ \"")
        pattern, *_ = args[0]

        return str.join("\n", [str(contact) for contact in self.address_book.search(pattern)])

    @input_error
    def get_all(self, *args) -> str:
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
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"show-birthday _name_ \"")
        name, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str(contact.birthday) if contact.birthday else f"{name} doesn\'t have birthday set"

    @input_error
    def birthdays(self, *args) -> str:
        if len(*args):
            raise IndexError("\"birthdays\" doesn\'t need arguments")
        birth_dict = self.address_book.get_upcoming_birthdays()
        result_str = ""
        for bd in birth_dict:
            result_str += f"{str(bd['name']) : <20}{bd['congratulation_date'] : <20}\n"
        return result_str

    @input_error
    def add_email(self, *args) -> str:
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
        """ Remove contact """
        name, *_ = args[0]
        self.address_book.delete(name)
        return f"Contact {name} removed."
    
    @input_error
    def notebook_mode(self):
        print("Welcome to NoteBook mode! Type 'exit' to go back.")
        exit_notebook = False

        while not exit_notebook:
            inp = input("notebook >> ").strip()
            command, *args = self.parse_input(inp)

            if command in ["exit", "close"]:
                exit_notebook = True
            elif command in self.note_handlers:
                print(self.note_handlers[command](args))
            else:
                print("Unknown command. Type 'help' to see available commands.")
    
    @input_error
    def add_note(self, args):
        if len(args) < 2:
            return "Usage: add-note [title] [content]"
        title, content = args[0], " ".join(args[1:])
        return self.note_book.add_note(title, content)

    @input_error
    def edit_note(self, args):
        if len(args) < 2:
            return "Usage: edit-note [title] [new_content]"
        title, new_content = args[0], " ".join(args[1:])
        return self.note_book.edit_note(title, new_content)

    @input_error
    def delete_note(self, args):
        if len(args) < 1:
            return "Usage: delete-note [title]"
        title = args[0]
        return self.note_book.delete_note(title)

    @input_error
    def search_notes(self, args):
        if len(args) < 1:
            return "Usage: search-notes [keyword]"
        keyword = " ".join(args)
        return self.note_book.search_notes(keyword)

    @input_error
    def show_all_notes(self, args):
        return self.note_book.show_all_notes()
    
    @input_error
    def add_tags(self, args):
        if len(args) < 2:
            return "Usage: add-tag [title] [tag1, tag2, ...]"
        title = args[0]
        tags = args[1:]
        return self.note_book.add_tags_to_note(title, tags)

    @input_error
    def remove_tag(self, args):
        if len(args) < 2:
            return "Usage: remove-tag [title] [tag]"
        title, tag = args[0], args[1]
        return self.note_book.remove_tag_from_note(title, tag)

    def search_by_tag(self, args):
        if len(args) < 1:
            return "Usage: search-by-tag [tag]"
        tag = args[0]
        return self.note_book.search_notes_by_tag(tag)

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
        funcs["delete"] = self.delete_record
        funcs["notebook"] = lambda _: self.notebook_mode()  # Переход в режим NoteBook
        funcs["exit"] = self.finalize
        funcs["close"] = self.finalize
        return funcs

    def register_note_handlers(self) -> dict:
        funcs = dict()
        funcs["add-note"] = self.add_note
        funcs["edit-note"] = self.edit_note
        funcs["delete-note"] = self.delete_note
        funcs["add-tags"] = self.add_tags
        funcs["remove-tag"] = self.remove_tag
        funcs["search-notes"] = self.search_notes
        funcs["search-by-tag"] = self.search_by_tag
        funcs["search-by-tags"] = lambda args: self.note_book.search_notes_by_tags(args)
        funcs["show-notes"] = self.show_all_notes
        return funcs
  