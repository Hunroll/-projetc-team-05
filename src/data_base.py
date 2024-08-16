from dataclasses import dataclass
import pickle
from src.AddressBook import AddressBook
from src.NoteBook import NoteBook

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
        with open(username + ".pkl", "wb") as f:
            pickle.dump(data_base, f)
            
    @staticmethod
    def load_data(username="guest"):
        try:
            with open(username + ".pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return DataBase(AddressBook(), NoteBook())  # Повернення нової адресної книги і блокнота, якщо файл не знайдено