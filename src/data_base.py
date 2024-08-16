import os
from dataclasses import dataclass
import pickle
from src.AddressBook import AddressBook
from src.NoteBook import NoteBook

USER_HOME = os.getenv('HOME') or os.getenv('USERPROFILE') or os.getenv('HOMEPATH')
CCNB_HOME = os.getenv('CCNB_HOME') or os.path.join(USER_HOME, '.ccnb')

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
        if not os.path.exists(CCNB_HOME):
            os.makedirs(CCNB_HOME)
        filepath = os.path.join(CCNB_HOME, username + ".pkl")
        with open(filepath, "wb") as f:
            pickle.dump(data_base, f)
        print(f"Data saved to {filepath}")
            
    @staticmethod
    def load_data(username="guest"):
        try:
            filepath = os.path.join(CCNB_HOME, username + ".pkl")
            with open(filepath, "rb") as f:
                print(f"Loading data from {filepath}")
                return pickle.load(f)
        except FileNotFoundError:
            return DataBase(AddressBook(), NoteBook())  # Повернення нової адресної книги і блокнота, якщо файл не знайдено