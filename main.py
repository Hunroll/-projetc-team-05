
from src.Bot import *
from src.AddressBook import *
from colorama import Style

def main_loop():
    try:
        exit = False

        bot = Bot(input("Enter login >>> "))
        handlers = bot.register_handlers()

        # Let's make nice and readable help message
        # List with available commands must be changed if added new functions
        command_list = [
            ("hello", "Greet the bot."),
            ("add [name] [phone]", "Add a new contact."),
            ("add-birthday [name] [DD.MM.YYYY]", "Add birthday to existing contact."),
            ("change [name] [phone]", "Change an existing contact's phone."),
            ("phone [name]", "Show the phone number of the contact."),
            ("show-birthday [name]", "Show the birthday of an existing contact."),
            ("all", "Show all contacts."),
            ("birthdays", "Show upcoming birthdays."),
            ("add-email [name] [email]", "Add email to existing contact."),
            ("add-address [name] [address]", "Add address to existing contact."),
            ("delete [name]", "Delete contact."),
            ("search [arg]", "Search contact."),
            ("exit || close", "Exit the bot."),
            ("add-note [title] [content]", "Add a new note."),
            ("edit-note [title] [new_content]", "Edit an existing note."),
            ("delete-note [title]", "Delete an existing note."),
            ("search-notes [keyword]", "Search for notes by keyword."),
            ("show-notes", "Show all notes."),
        ]

        max_len = max(len(cmd) for cmd, _ in command_list)

        command_list = (
            f"{Fore.LIGHTGREEN_EX}\nAvailable commands:\n" +
            "".join(f"{Fore.LIGHTYELLOW_EX}- {cmd.ljust(max_len)}{Style.RESET_ALL} - {desc}\n" for cmd, desc in command_list)
        )
        print(command_list)

        while not exit:
            inp = input("bot_shell >> ").strip()
            command, *args = bot.parse_input(inp)
            if (command in ["exit", "close"]):
                exit = True
            #no "else" because some handlers may be registered
            if (command in handlers):
                print(handlers[command](args) + Style.RESET_ALL)

    except Exception as err:
        print (f"Unexprected error: {err}")
        if (bot):
            print("Trying to save DB state.")
            bot.save_data()
        return None
    finally:
        print (Style.RESET_ALL)

        
if __name__ == "__main__":
    main_loop()