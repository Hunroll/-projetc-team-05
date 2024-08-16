import re
from datetime import datetime

class Validator:
    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        """Normalize phone numbers to standard format, leaving only digits and '+' symbol at the beginning (always returns number in format +380XXXXXXXXX)

        Args:
            phone_number (str): string with phone number in any format

        Returns:
            str: normalized phone number in format +380XXXXXXXXX

        Errors_handling:
            ValueError: if entered phone number doesn't match any of known formats.
                        Prints error message and suggests to enter phone number in correct format.
        """
        phone_number = re.sub(r'\D', '', phone_number)  # delete all non-digit characters
        if len(phone_number) == 10 and phone_number.startswith("0"):
            return f"+38{phone_number}"
        elif len(phone_number) == 12 and phone_number.startswith("38"):
            return f"+{phone_number}"
        else:
            raise ValueError(f"{phone_number} use invalid phone number format. \n"
                            f"Please use the format '0XXXXXXXXX' or '+380XXXXXXXXX'")

    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email address using regex. Raises ValueError if email is not valid.
            valid email: any symbols before @, any symbols before dot, 2-7 letters after last dot"""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(regex, email):
            raise ValueError(f"{email} is not a valid email address.")
        return email

    @staticmethod
    def validate_birthday(birthday: str) -> datetime:
        """Validate birthday date format and value. Raises ValueError if date is not valid.
            valid date format: DD.MM.YYYY
            valid date value: not 29 feb, not in future"""
        try:
            date = datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        # 29 february check
        if date.day == 29 and date.month == 2:
            raise ValueError("Birthday cannot be 29th February. Use 28.02.YYYY or 01.03.YYYY")
        # future date check
        if date > datetime.now():
            raise ValueError("Birthday can't be a future date")
        return date
