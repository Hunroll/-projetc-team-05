import re
from datetime import datetime, timedelta
from colorama import Fore, Style
from src.AddressBook import AddressBook
from src.models import *

CMD_EXIT="exit"
CMD_NA="n/a"
class Bot():
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

    #returns command key and args if any
    def parse_input(inp: str) -> tuple[str, tuple]:
        cmd, *args = inp.split()
        cmd = cmd.lower()
        return cmd, *args

    @input_error
    def say_hello(contacts: AddressBook, *args) -> str:
        if (len(*args)):
            raise IndexError("\"hello\" doesn\'t need arguments")
        return "How can I help you?"    

    @input_error
    def say_goodbye(contacts: AddressBook, *args) -> str:
        contacts.save_data()
        return "DB is saved. Good bye!"

    @input_error
    def add_contact(contacts: AddressBook, *args) -> str:
        if (len(*args) != 2):
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add _name_ _phone_\"")
        name, phone, *_ = args[0]
        mess = "Contact updated."
        contact = contacts.find(name)
        if not contact:
            contacts.add_record(Record(name))
            contact = contacts.find(name)
            mess = "Contact added."
        contact.add_phone(phone)
        return mess
        
    @input_error
    def change_contact(contacts: AddressBook, *args) -> str:
        if (len(*args) != 3):
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"change _name_ _old_phone_ _new_phone_\"")
        name, old_phone, new_phone, *_ = args[0]
        contact = contacts.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist, please use \"add {name} {new_phone}\"")

        contact.edit_phone(old_phone, new_phone)
        return "Contact updated."

    @input_error
    def get_phone(contacts: AddressBook, *args) -> str:
        if (len(*args) != 1):
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"phone _name_ \"")
        name, *_ = args[0]
        contact = contacts.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str.join("; ", contact.phones)

    @input_error
    def get_all(contacts: AddressBook, *args) -> str:
        if (len(*args)):
            raise IndexError("\"all\" doesn\'t need arguments")
        if (len(contacts) == 0):
            return "It\'s lonely here:( Please use \"add\" command"
        result_str = "{:<20} {:<12} {}\n".format("Name", "Birthday", "Phone(s)")
        for k, user in contacts.items():
            result_str += "{:<20} {:<12} {}\n".format(
                str(user.name), 
                str(user.birthday) if user.birthday else 'Not set', 
                '; '.join(user.phones) )
        return result_str

    @input_error
    def add_birthday(contacts: AddressBook, *args) -> str:
        if (len(*args) != 2):
            raise ValueError("Incorrect number of arguments." + Fore.YELLOW + " Please try \"add-birthday _name_ _DD.MM.YYYY_\"")
        name, birthday, *_ = args[0]
        
        contact = contacts.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        
        contact.add_birthday(birthday)
        return "Contact updated."
        
    @input_error
    def show_birthday(contacts: AddressBook, *args) -> str:
        if (len(*args) != 1):
            raise IndexError("Incorrect number of arguments" + Fore.YELLOW + " Please try \"show-birthday _name_ \"")
        name, *_ = args[0]
        contact = contacts.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        return str(contact.birthday) if contact.birthday else f"{name} doesn\'t have birthday set"

    @input_error
    def birthdays(contacts: AddressBook, *args) -> str:
        if (len(*args)):
            raise IndexError("\"birthdays\" doesn\'t need arguments")
        dict = contacts.get_upcoming_birthdays()
        result_str = ""
        for bd in dict:
            result_str += f"{str(bd['name']) : <20}{bd['congratulation_date'] : <20}\n"
        return result_str

    def register_handlers() -> dict:
        funcs = dict()
        funcs["hello"] = Bot.say_hello
        funcs["add"] = Bot.add_contact
        funcs["add-birthday"] = Bot.add_birthday
        funcs["change"] = Bot.change_contact
        funcs["phone"] = Bot.get_phone
        funcs["show-birthday"] = Bot.show_birthday
        funcs["all"] = Bot.get_all
        funcs["birthdays"] = Bot.birthdays
        funcs["exit"] = Bot.say_goodbye
        funcs["close"] = Bot.say_goodbye
        return funcs
