import functools  # Metadata import from function into decorator

from colorama import Fore, Style
from prompt_toolkit import PromptSession  # For autocomplete commands

from ccnb.src.AddressBook import AddressBook
from ccnb.src.NoteBook import NoteBook
from ccnb.src.data_base import DataBase, CorruptedFileException
from ccnb.src.models import *

CMD_EXIT="exit"
CMD_NA="n/a"
class Bot:
    """Bot class for handling user input and managing AddressBook and NoteBook
    Contains two handlers with commands and methods for handling them
    Attributes:
        current_user: str, current username
        address_book: AddressBook, instance of AddressBook
        note_book: NoteBook, instance of NoteBook
    Methods have explanation in docstrings.
    """
    
    current_user: str
    address_book: AddressBook
    note_book: NoteBook

    def __init__(self, user_name: str):
        self.__current_user = Validator.normalize_username(user_name)
        (database, password) = DataBase.load_data(self.current_user)
        self.address_book = database.address_book
        self.note_book = database.note_book
        self.password = password
    
        self.addressbook_handlers = self.register_addressbook_handlers()
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
        """Decorator for handling exceptions in input functions without breaking the program"""

        @functools.wraps(func)  # Get original metadata from functions
        def inner(*args, **kwargs) -> str:
            try:
                return func(*args, **kwargs) or ""
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
        """Parse input string into command and arguments
        inout string converts to command and list of arguments
        """
        cmd, *args = inp.split()
        cmd = cmd.lower()
        if cmd == "edit":
            # edit command has 2 arguments. First is multiple-words name of contact, second is field to edit
            try:
                # Splitting input into name and field. Name is all words except last, field is last word
                # Example: "edit John Doe phone" -> "edit", "John Doe", "phone"
                name, field = " ".join(args[:-1]), args[-1]
                return cmd, name, field
            except IndexError:
                # If not enough arguments provided, raise IndexError and return command without arguments
                return cmd, *args
        return cmd, *args
    
    @staticmethod
    @input_error
    def launcher(bot=None):
        """ Bot launcher """
        try:
            bot = Bot(input("Enter login >>> "))
            # First should be addressbook
            bot.addressbook_mode()
        except CorruptedFileException as err:
            print(f"Could not open save file. Error: {err}")
            return None
        except Exception as err:
            print(f"Unexpected error: {err}")
            if bot:
                print("Trying to save DB state.")
                bot.finalize([])
            return None
        finally:
            print (Style.RESET_ALL)

    @input_error
    def addressbook_mode(self, session=None, command_completer=None):
        """addressbook, Switch handler to addressbook mode."""
        """Start addressbook handlers and auto-feeling commands."""

        # Get addressbook handlers list
        handlers = self.addressbook_handlers
        addressbook_command_list = self.print_handlers_list(handlers)

        print("Welcome to Addressbook mode!")
        print(addressbook_command_list)

        is_prompt = True
        try:
            # guess user input
            session = PromptSession()
            handlers_command_list = list(handlers.keys())
            command_completer = CustomCommandCompleter(handlers_command_list)  
        except BaseException as err:
            print(f"Prompt feature error: {err}")
            is_prompt = False

        exit_ = False
        while not exit_:

            if is_prompt:
                inp = session.prompt("bot_shell >> ", completer=command_completer).strip()
            else:
                inp = input("bot_shell >> ").strip()

            # Skip empty input
            if inp == "":
                continue

            command, *args = self.parse_input(inp)
            if command in ["exit", "close"]:
                exit_ = True
            if command in handlers:
                print(handlers[command](args) + Style.RESET_ALL)
            else:
                print(f"{Fore.RED}Unknown command!{Style.RESET_ALL}")
        

    @input_error
    def notebook_mode(self, _, session=None, command_completer=None):
        """notebook, Switch to notebook."""
        
        # Get notebook handlers list
        handlers = self.note_handlers
        notebook_command_list = self.print_handlers_list(handlers)

        print("Welcome to NoteBook mode!")
        print(notebook_command_list)

        is_prompt = True
        try:
            # guess user input
            session = PromptSession()
            handlers_command_list = list(handlers.keys())
            command_completer = CustomCommandCompleter(handlers_command_list)
        except BaseException as err:
            print(f"Prompt feature error: {err}")
            is_prompt = False

        exit_ = False
        while not exit_:
            
            if is_prompt:
                inp = session.prompt("bot_shell >> ", completer=command_completer).strip()
            else:
                inp = input("bot_shell >> ").strip()

            # Skip empty input
            if inp == "":
                continue

            command, *args = self.parse_input(inp)
            if command in ["exit", "close", "main"]:
                exit_ = True
            elif command in handlers:
                print(handlers[command](args) + Style.RESET_ALL)
            else:
                print(f"{Fore.RED}Unknown command!{Style.RESET_ALL}")
                
        return "Navigated back to main menu."

    @input_error
    def say_hello(self, *args) -> str:
        """hello, Greet the bot."""
        if len(*args):
            raise IndexError("\"hello\" doesn\'t need arguments")
        return f"How can I help you, {self.current_user}?"

    @input_error
    def finalize(self, *args) -> str:
        """exit || close, Exit the bot."""
        DataBase.save_data(self.address_book, self.note_book, self.current_user, self.password)
        return "DB is saved. Good bye!"

    @input_error
    def add_contact(self, *args) -> str:
        """add [name] [phone], Add a new contact."""
        if len(*args) != 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add _name_ _phone_\"")
        name, phone = args[0]
        mess = "Contact already exist. Just updated with new phone."
        contact = self.address_book.find(name)
        if not contact:
            self.address_book.add_record(UserRecord(name))
            contact = self.address_book.find(name)
            mess = "Contact added."
        contact.add_phone(phone)
        return mess

    @input_error
    def get_phone(self, *args) -> str:
        """phone [name], Show the phone number of the contact."""
        name = " ".join(args[0])
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str.join("; ", contact.phones)

    @input_error
    def search_contact(self, *args) -> str:
        """search [pattern], Search contact by pattern in all fields. Field order: name, phone, birthday, email, address."""
        pattern = " ".join(args[0])

        search_result = self.address_book.search(pattern)
        if search_result:
            return str.join("\n\n", [str(contact) for contact in self.address_book.search(pattern)])
        return "No matches"

    @input_error
    def get_all(self, *args) -> str:
        """all, Show all contacts."""
        if len(*args):
            raise IndexError("\"all\" doesn\'t need arguments")
        if len(self.address_book) == 0:
            return "It\'s lonely here:( Please use \"add\" command"
        result_str = "{:<20} {:<12} {:<20} {:<20} {:<20}\n".format("Name", "Birthday", "Phone(s)", "Email(s)",
                                                                   "Address")
        for k, user in self.address_book.items():
            result_str += "{:<20} {:<12} {:<20} {:<20} {:<20}\n".format(
                str(user.name),
                str(user.birthday) if user.birthday else 'Not set',
                UserRecord.truncate_list_of_recs(user.phones),
                UserRecord.truncate_list_of_recs(user.emails),
                str(user.address) if user.address else 'Not set')
        return result_str

    @input_error
    def add_birthday(self, *args) -> str:
        """add-birthday [name] [DD.MM.YYYY], Add birthday to existing contact."""
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
        """show-birthday [name], Show the birthday of an existing contact."""
        if len(*args) != 1:
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"show-birthday _name_ \"")
        name, *_ = args[0]
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str(contact.birthday) if contact.birthday else f"{name} doesn\'t have birthday set"

    @input_error
    def birthdays(self, *args) -> str:
        """birthdays [days], Show upcoming birthdays. (optional) show only upcoming [days] days"""
        if len(*args) > 1:
            raise IndexError("\"birthdays\" can only accept 1 argument - number of days")
        if (args[0]):
            days = int(args[0][0])
        else:
            days = 7
        birth_dict = self.address_book.get_upcoming_birthdays(days=days)
        if not birth_dict:
            raise KeyError("Nothing to show")
        result_str = ""
        for bd in birth_dict:
            result_str += f"{str(bd['name']) : <20}{bd['congratulation_date'] : <20}\n"
        return result_str

    @input_error
    def add_email(self, *args) -> str:
        """add-email [name] [email], Add email to existing contact."""
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
        """add-address [name] [address], Add address to existing contact."""
        if len(*args) < 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add-address _name_ _address_\"")

        name, *address_parts = args[0]
        address = ' '.join(address_parts)
        
        contact = self.address_book.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        
        contact.address = address
        return "Contact updated."

    @input_error
    def edit_contact(self, *args) -> str:
        """edit [name] [field], Edit contact information."""
        if len(*args) < 2:
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"edit _name_ _field_\"")
        name, field, *_ = args[0]
        contact = self.address_book.find(name)
        field = field.lower()  # lowercase field name for comparison
        if not contact:
            raise KeyError(f"Contact {name} doesn\'t exist")
        match field:
            case "phone":
                old_phone = Validator.normalize_phone(input("Enter phone number to edit: "))
                if old_phone not in contact.phones:
                    raise ValueError("Phone number not found")
                new_phone = input("Enter new phone number: ")
                contact.edit_phone(old_phone, new_phone)
            case "email":
                if contact.emails is None or len(contact.emails) == 0:
                    raise KeyError('Nothing to edit. Please use "add-email" command')
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
        return "Contact updated\n"

    @input_error
    def delete_record(self, *args) -> str:
        """delete [name], Delete contact."""
        name, *_ = args[0]
        self.address_book.delete(name)
        return f"Contact {name} removed."
    
    @input_error
    def set_password(self, *args) -> str:
        """set-password [new_pass], Set password."""
        if len(*args) < 1:
            raise ValueError("Password can\'t be empty.")
        new_passwd = " ".join(args[0])

        delete_unenctypted = (new_passwd and not self.password) # delete old file .pkl if password is set

        self.password = new_passwd
        DataBase.save_data(self.address_book, self.note_book, self.current_user, self.password)
        if delete_unenctypted:
            DataBase.delete_unencrypted_save(self.current_user)
        return f"Password changed successfully."
    
    @input_error
    def add_note(self, *args):
        """add [title] [content], Add a new note."""
        if len(*args) < 2:
            return "Usage: add-note [title] [content]"
        title, *content_parts = args[0]
        content = " ".join(content_parts)
        return self.note_book.add_note(title, content)

    @input_error
    def edit_note(self, *args):
        """edit [title] [new_content], Edit an existing note."""
        if len(*args) < 2:
            return "Usage: edit [title] [new_content]"
        title, *new_content_parts = args[0]
        new_content = " ".join(new_content_parts)
        return self.note_book.edit_note(title, new_content)

    @input_error
    def delete_note(self, *args):
        """delete [title], Delete an existing note."""
        if len(*args) < 1:
            return "Usage: delete [title]"
        title, *_ = args[0]
        return self.note_book.delete_note(title)

    @input_error
    def search_notes(self, *args):
        """search [keyword], Search for notes by keyword."""
        if len(*args) < 1:
            return "Usage: search-notes [keyword]"
        keyword = " ".join(*args)
        return self.note_book.search_notes(keyword)

    @input_error
    def show_all_notes(self, *args):
        """all, Show all notes."""
        return self.note_book.show_all_notes()
    
    @input_error
    def add_tags(self, *args):
        """add-tags [title] [tag1 tag2 ...], Add tags to the note. All tags should be separated by space."""
        if len(*args) < 2:
            return "Usage: add-tags [title] [tag1 tag2 ...]"
        title, *tags = args[0]
        return self.note_book.add_tags_to_note(title, tags)

    @input_error
    def remove_tag(self, *args):
        """remove-tag [title] [tag1 tag2 ...], Remove certain tags from the note. All tags should be separated by space."""
        if len(*args) < 2:
            return "Usage: remove-tag [title] [tag]"
        title, *tags = args[0]
        return "\n".join(self.note_book.remove_tag_from_note(title, tag) for tag in tags)

    @input_error
    def search_by_tags(self, *args):
        """search-by-tags [tag1 tag2 ...], Show notes filtered by tags count. All tags should be separated by space."""
        if len(*args) < 1:
            return "Usage: search-by-tags [tag1 tag2 ...]"
        tags = args[0]
        return self.note_book.search_notes_by_tags(tags)
    
    @input_error
    def sort_notes_by_tag_count(self, *args):
        """sort-by-tags-count, Show notes sorted by tags count."""
        return self.note_book.sort_notes_by_tag_count()

    @input_error
    def sort_notes_by_tags_alphabetically(self, *args):
        """sort-by-tags-alphabetically, Show notes sorted by tags alphabetically."""
        return self.note_book.sort_notes_by_tags_alphabetically()
    
    @input_error
    def help_text_addressbook(self, *args):
        """help, Show addressbook command list"""
        command_list = self.print_handlers_list(self.addressbook_handlers)
        return print(command_list)
    
    @input_error
    def help_text_notebook(self, *args):
        """help, Show notebook command list"""
        command_list = self.print_handlers_list(self.note_handlers)
        return print(command_list)
    
    @input_error
    def stop_notebook(self, *args):
        """close | exit | main, Close notebook and return to main menu"""
        pass
      
    def register_addressbook_handlers(self) -> dict:
        """Addressbook handlers."""
        funcs = dict()
        funcs["hello"] = self.say_hello
        funcs["notebook"] = self.notebook_mode  # Переход в режим NoteBook
        funcs["add"] = self.add_contact
        funcs["add-birthday"] = self.add_birthday
        funcs["phone"] = self.get_phone
        funcs["show-birthday"] = self.show_birthday
        funcs["all"] = self.get_all
        funcs["birthdays"] = self.birthdays
        funcs["add-email"] = self.add_email
        funcs["add-address"] = self.add_address
        funcs["search"] = self.search_contact
        funcs["edit"] = self.edit_contact
        funcs["delete"] = self.delete_record
        funcs["set-password"] = self.set_password
        funcs["exit"] = self.finalize
        funcs["close"] = self.finalize
        funcs["help"] = self.help_text_addressbook
        return funcs

    def register_note_handlers(self) -> dict:
        """Notebook handlers."""
        funcs = dict()
        funcs["add"] = self.add_note
        funcs["edit"] = self.edit_note
        funcs["delete"] = self.delete_note
        funcs["add-tags"] = self.add_tags
        funcs["remove-tag"] = self.remove_tag
        funcs["search"] = self.search_notes
        funcs["search-by-tags"] = self.search_by_tags
        funcs["all"] = self.show_all_notes
        funcs["sort-by-tags-count"] = self.sort_notes_by_tag_count
        funcs["sort-by-tags-alphabetically"] = self.sort_notes_by_tags_alphabetically
        funcs["help"] = self.help_text_notebook
        funcs["exit"] = self.stop_notebook
        funcs["close"] = self.stop_notebook
        funcs["main"] = self.stop_notebook

        return funcs

    def print_handlers_list(self, handlers) -> str:
        """Handler's list for hello message"""
        command_descriptions = []
        seen_commands = set()

        # Get all functions descriptions
        for _, func in handlers.items():
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

