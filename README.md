# CLI contacts and notes bot (CNNB)

![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FHunroll%2F-projetc-team-05%2Fmain%2Fpyproject.toml&query=%24.title&style=plastic&label=name)
![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FHunroll%2F-projetc-team-05%2Fmain%2Fpyproject.toml&query=%24.project.name&style=plastic&logo=https%3A%2F%2Ftest.pypi.org%2Fstatic%2Fimages%2Flogo-small.8998e9d1.svg&label=short-name&labelColor=lightgray&color=darkblue)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FHunroll%2F-projetc-team-05%2Fmain%2Fpyproject.toml&query=%24.project.version&style=plastic&label=pypi&color=green)](https://test.pypi.org/project/ccnb/)
![Python Version](https://img.shields.io/badge/python-3.10%2B-orange?labelColor=blue&style=plastic)
[![License](https://img.shields.io/badge/license-MIT-blue?style=plastic)](LICENSE)

### Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Introduction:

This is a simple CLI contacts and notes bot that allows you to store and retrieve contacts and notes. It is written in Python for team project on GoIT Neoversity Master of Science in Sybersecurity course.

## Features:

#### Storage:
store contacts and notes in a local binary file \<username>.pkl

#### Contacts:

Manage your contacts with the following commands:

| Command                            | Description                                                                                       |
|------------------------------------|---------------------------------------------------------------------------------------------------|
| `hello`                            | Greet the bot.                                                                                    |
| `notebook`                         | Switch handler to notebook mode.                                                                  |
| `add [name] [phone]`               | Add a new contact.                                                                                |
| `add-birthday [name] [DD.MM.YYYY]` | Add birthday to existing contact.                                                                 |
| `phone [name]`                     | Show the phone number of the contact.                                                             |
| `show-birthday [name]`             | Show the birthday of an existing contact.                                                         |
| `all`                              | Show all contacts.                                                                                |
| `birthdays`                        | Show upcoming birthdays.                                                                          |
| `add-email [name] [email]`         | Add email to existing contact.                                                                    |
| `add-address [name] [address]`     | Add address to existing contact.                                                                  |
| `search [pattern]`                 | Search contact by pattern in all fields. <br/>Field order: name, phone, birthday, email, address. |
| `edit [name] [field]`              | Edit contact information.                                                                         |
| `delete [name]`                    | Delete contact.                                                                                   |
| `exit` `close`                     | Exit the bot.                                                                                     |
| `help`                             | Show addressbook command list                                                                     |

#### Notes:

After switching to notebook mode, you can manage your notes with the following commands:

| Command                              | Description                               |
|--------------------------------------|-------------------------------------------|
| `add [title] [content]`              | Add a new note.                           |
| `edit [title] [new_content]`         | Edit an existing note.                    |
| `delete [title]`                     | Delete an existing note.                  |
| `add-tag [title] [tag1 tag2 ...]`    | Add tags to the note.*                    |
| `remove-tag [title] [tag1 tag2 ...]` | Remove certain tags from the note.*       |
| `search [keyword]`                   | Search for notes by keyword.              |
| `search-by-tags [tag1 tag2 ...]`     | Show notes filtered by tags count.*       |
| `all`                                | Show all notes.                           |
| `sort-by-tags-count`                 | Show notes sorted by tags counts.         |
| `sort-by-tags-alphabetically`        | Show notes sorted by tags alphabetically. |
| `help`                               | Show notebook command list                |
| `close` `exit` `main`                | Close notebook and return to main menu    |

**\*Note:** All multiple-tags in commands should be separated by space.

## Installation:

### Requirements:

For installing the bot you need to have Python 3.10 or higher installed on your machine.

[Instructions on how to install Python](https://www.python.org/downloads/).

### Dependencies

| package        | minimum version |
|----------------|-----------------|
| colorama       | 0.4.4           |
| prompt-toolkit | 3.0.20          |

#### To install the bot you can use the following command:

```bash
pip install -i https://test.pypi.org/simple/ ccnb
```

#### Alternatively, you can clone the repository and install the bot from the source code:

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
\Users\\\<username>\\.ccnb).
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
