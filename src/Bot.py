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
    def parse_input(inp: str) -> tuple[str, str, str] | tuple[str, Any]:
        cmd, *args = inp.split()
        cmd = cmd.lower()
        if cmd == "edit":
            name, field = " ".join(args[:-1]), args[-1]
            return cmd, name, field
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
        name = " ".join(args[0])
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
                '; '.join(user.emails) if user.emails else 'Not set',
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
        
        contact.birthday = birthday
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
    def edit_contact(self, *args) -> str:
        """
        Edit contact field
        first receive name of contact and name of field to edit
        reask for field value to edit with additional dialog with user
        """
        if len(*args) < 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"edit _name_ _field_\"")
        name, field, *_ = args[0]
        contact = self.address_book.find(name)
        field = field.lower()  # lowercase field name for comparison
        if not contact:
            raise KeyError(f"Contact {name} doesn\'t exist")
        match field:
            case "phone":
                old_phone = normalize_phone(input("Enter phone number to edit: "))
                if old_phone not in contact.phones:
                    raise ValueError("Phone number not found")
                new_phone = input("Enter new phone number: ")
                contact.edit_phone(old_phone, new_phone)
            case "email":
                old_email = input("Enter email to edit: ")
                if old_email not in contact.emails:
                    raise ValueError("Email not found")
                new_email = input("Enter new email: ")
                contact.edit_email(old_email, new_email)
            case "address":
                new_address = input("Enter new address: ")
                contact.address = new_address
            case "birthday":
                new_birthday = input("Enter new birthday: ")
                contact.birthday = new_birthday
            case "name":
                new_name = input("Enter new name: ")
                contact.name = new_name
            case _:
                raise ValueError("Incorrect field to edit. \nPlease use name of field:\n" + Fore.YELLOW + " \t \"name\", \"birthday\", \"phone\", \"email\" or \"address\"")
        return "Contact updated"

    @input_error
    def delete_record(self, *args) -> str:
        '''delete-contact [name], Delete contact.'''
        """ Remove contact """
        name, *_ = args[0]
        self.address_book.delete(name)
        return f"Contact {name} removed."
    
    @input_error
    def notebook_mode(self, _):
        notebook_command_list = [
            ("add-note [title] [content]", "Add a new note."),
            ("edit-note [title] [new_content]", "Edit an existing note."),
            ("delete-note [title]", "Delete an existing note."),
            ("add-tags [title] [tag1, tag2, ...]", "Add tags to a note."),
            ("remove-tag [title] [tag]", "Remove a tag from a note."),
            ("search-notes [keyword]", "Search for notes by keyword."),
            ("search-by-tags [tag1, tag2, ...]", "Search for notes by tags."),
            ("show-notes", "Show all notes."),
            ("exit || close || main", "Exit NoteBook mode and return to main menu."),
        ]
        max_len = max(len(cmd) for cmd, _ in notebook_command_list)
        notebook_command_list = (
            f"{Fore.LIGHTGREEN_EX}\nAvailable commands:\n" +
            "".join(f"{Fore.LIGHTYELLOW_EX}- {cmd.ljust(max_len)}{Style.RESET_ALL} - {desc}\n" for cmd, desc in notebook_command_list)
        )
        print("Welcome to NoteBook mode!")
        print(notebook_command_list)
        exit_notebook = False

        while not exit_notebook:
            inp = input("notebook >> ").strip()
            command, *args = self.parse_input(inp)

            if command in ["exit", "close", "main"]:
                exit_notebook = True
            elif command in self.note_handlers:
                print(self.note_handlers[command](args))
            else:
                print(f"{Fore.RED}Unknown command!{Style.RESET_ALL}")
                print(notebook_command_list)
        return "Navigating back to main menu."
    
    @input_error
    def add_note(self, args):
        '''add-note [title] [content], Add a new note.'''
        if len(args) < 2:
            return "Usage: add-note [title] [content]"
        title, content = args[0], " ".join(args[1:])
        return self.note_book.add_note(title, content)

    @input_error
    def edit_note(self, args):
        '''edit-note [title] [new_content], Edit an existing note.'''
        if len(args) < 2:
            return "Usage: edit-note [title] [new_content]"
        title, new_content = args[0], " ".join(args[1:])
        return self.note_book.edit_note(title, new_content)

    @input_error
    def delete_note(self, args):
        '''delete-note [title], Delete an existing note.'''
        if len(args) < 1:
            return "Usage: delete-note [title]"
        title = args[0]
        return self.note_book.delete_note(title)

    @input_error
    def search_notes(self, args):
        '''search-notes [keyword], Search for notes by keyword.'''
        if len(args) < 1:
            return "Usage: search-notes [keyword]"
        keyword = " ".join(args)
        return self.note_book.search_notes(keyword)

    @input_error
    def show_all_notes(self, args):
        '''show-notes, Show all notes.'''
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

    @input_error
    def search_by_tags(self, args):
        if len(args) < 1:
            return "Usage: search-by-tag [tag1, tag2, ...]"
        return self.note_book.search_notes_by_tags(args)
      
    def register_handlers(self) -> dict:
        # If you added new function, update Help text in /main.py
        funcs = dict()
        funcs["hello"] = self.say_hello
        funcs["add"] = self.add_contact
        funcs["add-birthday"] = self.add_birthday
        funcs["change"] = self.change_contact  # MARK TO DELETE
        funcs["phone"] = self.get_phone
        funcs["show-birthday"] = self.show_birthday
        funcs["all"] = self.get_all
        funcs["birthdays"] = self.birthdays
        funcs["add-email"] = self.add_email
        funcs["add-address"] = self.add_address
        funcs["search"] = self.search_contact
        funcs["edit"] = self.edit_contact
        funcs["delete-contact"] = self.delete_record
        funcs["notebook"] = self.notebook_mode  # Переход в режим NoteBook
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
        funcs["search-by-tags"] = self.search_by_tags
        funcs["show-notes"] = self.show_all_notes
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
  
  
