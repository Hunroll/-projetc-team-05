import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from pyAesCrypt import encryptStream, decryptStream
from colorama import Fore
import getpass
import io

from ccnb.src.AddressBook import AddressBook
from ccnb.src.NoteBook import NoteBook

USER_HOME = os.getenv('HOME') or os.getenv('USERPROFILE') or os.getenv('HOMEPATH')
CCNB_PATH = os.getenv('CCNB_PATH')
if CCNB_PATH and Path(CCNB_PATH).is_file():
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
        - save_data(address_book: AddressBook, note_book: NoteBook, username, password="")
            saves data to a file named by username
        - load_data(username="guest") -> (DataBase, str)
            loads data from a file or returns new AddressBook and NoteBook if file not found. Second return value is user's password
        - delete_unencrypted_save(username) 
            deletes unencrypted pickle file when user sets password data from a file or returns new AddressBook and NoteBook if file not found
    """
    address_book: AddressBook
    note_book: NoteBook

    @staticmethod
    def save_data(address_book: AddressBook, note_book: NoteBook, username, password=""):
        data_base = DataBase(address_book, note_book)
        if not os.path.exists(CCNB_PATH):
            try:
                os.makedirs(CCNB_PATH)
            except OSError:
                print(
                    Fore.RED + "[ERROR] " + Fore.YELLOW + f"Creation of the directory {CCNB_PATH} failed" + Fore.RESET)
        filepath = os.path.join(CCNB_PATH, username.lower() + ".pkl")
        if not password:
            with open(filepath, "wb") as plain_file:
                pickle.dump(data_base, plain_file)
        else:
            filepath = filepath + ".aes"
            plain_stream = pickle.dumps(data_base)
            encrypted_stream = io.BytesIO()
            encryptStream(io.BytesIO(plain_stream), encrypted_stream, password, 64 * 1024)
            with open(filepath, "wb") as encrypted_file:
                encrypted_file.write(encrypted_stream.getvalue())

        print(Fore.BLUE + "[INFO] " + Fore.YELLOW + f"Data saved to {filepath}" + Fore.RESET)

    @staticmethod
    def delete_unencrypted_save(username):
        filepath = os.path.join(CCNB_PATH, username.lower() + ".pkl")
        if os.path.exists(filepath):
            os.remove(filepath)
            print(Fore.BLUE + "[INFO] " + Fore.YELLOW + f"Unencrypted save file {filepath} was deleted" + Fore.RESET)
            
    @staticmethod
    def load_data(username="guest"):
        try:
            filepath = os.path.join(CCNB_PATH, username.lower() + ".pkl")
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    print(Fore.BLUE + "[INFO] " + Fore.YELLOW + f"Loading data from {filepath}" + Fore.RESET)
                    return pickle.load(f)
            elif os.path.exists(filepath + ".aes"):
                filepath = filepath + ".aes"
                retries = 3
                while retries > 0:
                    password = getpass.getpass('Password: ')
                    try:
                        with open(filepath, "rb") as encrypted_file:
                            encrypted_stream = encrypted_file.read()
                        plain_stream = io.BytesIO()
                        decryptStream(io.BytesIO(encrypted_stream), plain_stream, password, 64 * 1024)
                        return (pickle.loads(plain_stream.getvalue()), password)
                    except Exception as ex:
                        retries -= 1
                        print(Fore.RED + "Wrong password. " + Fore.YELLOW + f"Retries left: {retries}" + Fore.RESET)
                raise CorruptedFileException("Wrong password or file is corrupted")
            else:
                return (DataBase(AddressBook(), NoteBook()), None)
        except CorruptedFileException as cfe:
            raise cfe
        except Exception as ex:
            raise Exception("Error opening save file!", ex)

class CorruptedFileException(Exception):
    pass