import os
import pickle
from dataclasses import dataclass
from pathlib import Path

from colorama import Fore

from ccnb.src.AddressBook import AddressBook
from ccnb.src.NoteBook import NoteBook

USER_HOME = os.getenv('HOME') or os.getenv('USERPROFILE') or os.getenv('HOMEPATH')
CCNB_PATH = os.getenv('CCNB_PATH')
if Path(CCNB_PATH).is_file():
    print(Fore.RED + "[ERROR] " + Fore.YELLOW +
          f"\t{CCNB_PATH} is a file, not a directory\n"
          f"\t\tPlease, set CCNB_PATH to a directory" + Fore.RESET)
    CCNB_PATH = os.path.join(USER_HOME, '.ccnb')
    print(Fore.YELLOW + f"\t\tUsing default path: {CCNB_PATH}\n" + Fore.RESET)
elif CCNB_PATH is None:
    CCNB_PATH = os.path.join(USER_HOME, '.ccnb')

@dataclass
class DataBase:
    """Class for storing and reading data to/from file.
    Supported operations:
        - save_data(address_book: AddressBook, note_book: NoteBook, username="guest")
            saves data to a file named by username
        - load_data(username="guest") -> DataBase
            loads data from a file or returns new AddressBook and NoteBook if file not found
    """
    address_book: AddressBook
    note_book: NoteBook

    @staticmethod
    def save_data(address_book: AddressBook, note_book: NoteBook, username="guest"):
        data_base = DataBase(address_book, note_book)
        if not os.path.exists(CCNB_PATH):
            try:
                os.makedirs(CCNB_PATH)
            except OSError:
                print(
                    Fore.RED + "[ERROR] " + Fore.YELLOW + f"Creation of the directory {CCNB_PATH} failed" + Fore.RESET)
        filepath = os.path.join(CCNB_PATH, username.lower() + ".pkl")
        with open(filepath, "wb") as f:
            pickle.dump(data_base, f)
        print(Fore.BLUE + "[INFO] " + Fore.YELLOW + f"Data saved to {filepath}" + Fore.RESET)
            
    @staticmethod
    def load_data(username="guest"):
        try:
            filepath = os.path.join(CCNB_PATH, username.lower() + ".pkl")
            with open(filepath, "rb") as f:
                print(Fore.BLUE + "[INFO] " + Fore.YELLOW + f"Loading data from {filepath}" + Fore.RESET)
                return pickle.load(f)
        except FileNotFoundError:
            # Return new AddressBook and NoteBook if file not found
            return DataBase(AddressBook(), NoteBook())
