
from src.Bot import *
from src.AddressBook import *
from colorama import Style

def main_loop():
    try:
        exit = False
        handlers = Bot.register_handlers()
        contacts = AddressBook.load_data()
        print("Welcome to the assistant bot!")
        while not exit:
            inp = input("bot_shell >> ").strip()
            command, *args = Bot.parse_input(inp)
            if (command in ["exit", "close"]):
                exit = True
            #no "else" because some handlers may be registered
            if (command in handlers):
                print(handlers[command](contacts, args) + Style.RESET_ALL)

    except Exception as err:
        print (f"Unexprected error: {err}")
        print("Trying to save DB state.")
        contacts.save_data()
        return None
    finally:
        print (Style.RESET_ALL)

        
if __name__ == "__main__":
    main_loop()