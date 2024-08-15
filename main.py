
from src.Bot import *
from src.AddressBook import *
from colorama import Style
from prompt_toolkit import PromptSession # For autocomplete commands


def main_loop():
    # Autocomplete session
    try:
        exit_ = False

        bot = Bot(input("Enter login >>> "))
        handlers = bot.register_handlers()

        # Let's make nice and readable help message
        # TODO: Add subloop for notes
        print(bot.print_handlers_list())

        # guess user input
        session = PromptSession()
        handlers_command_list = list(handlers.keys())
        command_completer = CustomCommandCompleter(handlers_command_list)  

        while not exit_:
            inp = session.prompt("bot_shell >> ", completer=command_completer).strip()
            
            command, *args = bot.parse_input(inp)
            if command in ["exit", "close"]:
                exit_ = True
            #no "else" because some handlers may be registered
            if command in handlers:
                print(handlers[command](args) + Style.RESET_ALL)

    except Exception as err:
        print(f"Unexpected error: {err}")
        if bot:
            print("Trying to save DB state.")
            # TODO: Adding valid save_data method
            # bot.save_data()
        return None
    finally:
        print (Style.RESET_ALL)

        
if __name__ == "__main__":
    main_loop()