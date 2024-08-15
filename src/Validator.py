import re
from datetime import datetime

class Validator:
    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        """Нормалізує телефонні номери до стандартного формату, залишаючи тільки цифри та символ '+' на початку (завжди повертає номер у форматі +380XXXXXXXXX)

        Args:
            phone_number (str): рядок номера телефону у будь-якому форматі

        Returns:
            str: нормалізований номер телефону у форматі +380XXXXXXXXX

        Errors_handling:
            ValueError: якщо введений номер телефону не відповідає жодному з відомих форматів. Виводить повідомлення про помилку та пропонує ввести номер телефону у правильному форматі.
        """
        phone_number = re.sub(r'\D', '', phone_number)  # видалення всіх символів, що не є цифрами
        if len(phone_number) == 10 and phone_number.startswith("0"):  # перевірка, чи введений номер телефону має 10 цифр
            # та починається з '0'
            return f"+38{phone_number}"
        elif len(phone_number) == 12 and phone_number.startswith(
                "38"):  # перевірка, чи введений номер телефону має 12 цифр та починається з '38'
            return f"+{phone_number}"
        else:
            raise ValueError(f"{phone_number} use invalid phone number format. \n"
                            f"Please use the format '0XXXXXXXXX' or '+380XXXXXXXXX'")

    @staticmethod
    def validate_email(email: str) -> str:
        """Валідатор для електронних адрес. Повертає email або піднімає ValueError."""
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.match(regex, email):
            raise ValueError(f"{email} is not a valid email address.")
        return email

    @staticmethod
    def validate_birthday(birthday: str) -> datetime:
        """Валідатор для дати народження. Повертає дату у форматі datetime або піднімає ValueError."""
        try:
            date = datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        if date > datetime.now():
            raise ValueError("Birthday can't be a future date")
        return date
