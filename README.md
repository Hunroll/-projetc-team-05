# CLI contacts and notes bot (CNNB)

This is a simple CLI contacts and notes bot that allows you to store and retrieve contacts and notes.

## Introduction:

This is a simple CLI contacts and notes bot that allows you to store and retrieve contacts and notes. It is written in Python for team project on GoIT Neoversity Master of Science in Sybersecurity course.

## Features:

#### Storage:
store contacts and notes in a local binary file \<username>.pkl

#### Contacts:
Available commands:

- `hello`
    - Greet the bot.
- `add [name] [phone]`
    - Add a new contact.
- `add-birthday [name] [DD.MM.YYYY]`
    - Add birthday to existing contact.
- `edit [name] [field]`
    - Change an existing contact's phone. field could be "name", "birthday", "phone", "email" or "address"
- `phone [name]`
    - Show the phone number of the contact.
- `show-birthday [name]`
    - Show the birthday of an existing contact.
- `all`
    - Show all contacts.
- `birthdays`
    - Show upcoming birthdays.
- `add-email [name] [email]`
    - Add email to existing contact.
- `add-address [name] [address]`
    - Add address to existing contact.
- `search [arg]`
    - Search contact.
- `delete [name]`
    - Delete contact.
- `exit` || `close`
    - Exit the bot.

#### Notes:
Available commands:

- `add [title] [content]`
  - Add a new note.
- `edit [title] [new_content]`
  - Edit an existing note.
- `delete [title]`
  - Delete an existing note.
- `add-tags [title] [tag1 tag2 ...]`
  - Add tags to a note.
- `remove-tag [title] [tag]`
  - Remove a tag from a note.
- `search [keyword]`
  - Search for notes by keyword.
- `search-by-tags [tag1 tag2 ...]`
  - Search for notes by tags.
- `all`
  - Show all notes.
- `exit` || `close` || `main`
  - Exit NoteBook mode and return to main menu.

## Installation:

For installing the bot you need to have Python 3.10 or higher installed on your machine.

[Instructions on how to install Python](https://www.python.org/downloads/).

To install the bot you can use the following command:

```bash
pip install -i https://test.pypi.org/simple/ ccnb
```

Alternatively, you can clone the repository and install the bot from the source code:

```bash
git clone https://github.com/Hunroll/-projetc-team-05.git
cd -projetc-team-05
pip install -e .
```

## Usage:

To run the bot you can use the following command:

#### Windows:

```bash windows
py -m ccnb
```

#### Linux/MacOS:

```bash linux
python3 -m ccnb 
```

By default, the bot will create a new file with the name of the user in the system user directory (e.g. ~/.ccnb or C:
\Users\<username>\.ccnb).
You can use custom path to save database file by setting the environment variable CCNB_PATH to the desired directory.

Commands to set the environment variable:

#### Windows PowerShell:

```bash powershell
$ENV:CCNB_PATH = "path/to/your/directory"
```

#### Windows CMD:

```bash windows cmd
set CCNB_PATH=path/to/your/directory
```

#### Linux/MacOS:

```bash linux
export CCNB_PATH="path/to/your/directory"
```

## Contributors:
- [Huroll](https://github.com/Hunroll)
- [etosomsemnefiltry](https://github.com/etosomsemnefiltry)
- [Guru01100101](https://github.com/Guru01100101)
- [valerii-derkach](https://github.com/valerii-derkach)
- [bilancdt](https://github.com/bilancdt)

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
