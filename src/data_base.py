import os
import pickle
from dataclasses import dataclass
from pathlib import Path

from src.AddressBook import AddressBook
from src.NoteBook import NoteBook

USER_HOME = os.getenv('HOME') or os.getenv('USERPROFILE') or os.getenv('HOMEPATH')
# CCNB_PATH use for environment variable, if it is not set, then use default path
# if CCNB_PATH is file then use default path too
if os.getenv('CCNB_PATH') is None or Path(os.getenv('CCNB_PATH')).is_file():
    CCNB_PATH = os.path.join(USER_HOME, '.ccnb')
else:
    CCNB_PATH = os.getenv('CCNB_PATH')

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
                print(f"[ERROR] Creation of the directory {CCNB_PATH} failed")
        filepath = os.path.join(CCNB_PATH, username + ".pkl")
        with open(filepath, "wb") as f:
            pickle.dump(data_base, f)
        print(f"[LOG] Data saved to {filepath}")
            
    @staticmethod
    def load_data(username="guest"):
        try:
            filepath = os.path.join(CCNB_PATH, username + ".pkl")
            with open(filepath, "rb") as f:
                print(f"[LOG] Loading data from {filepath}")
                return pickle.load(f)
        except FileNotFoundError:
            return DataBase(AddressBook(), NoteBook())  # Повернення нової адресної книги і блокнота, якщо файл не знайдено