from datetime import datetime, timedelta
from collections import UserDict
from src.models import *
import pickle

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        if key in self.data:
            raise KeyError("Contact already exists")
        self.data[key] = record

    def find(self, name: str) -> Record:
        return self.data[name] if name in self.data else None
    
    def delete(self, name: str):
        if name not in self.data:
            raise KeyError("Contact doesn\'t exist")
        self.data.pop(name)

    def get_upcoming_birthdays(self, specific_date = None):
        result_set = []
        today = datetime.strptime(specific_date, "%d.%m.%Y").date() if specific_date != None else datetime.today().date()
        users_with_bd = list(v for (k, v) in self.data.items() if v.birthday)
        for user in users_with_bd:
            original_date = user.birthday.value.date()
            
            # Get this year's date
            try:
                date_this_year = original_date.replace(year = today.year)
            except:
                #29th of Feb
                date_this_year = datetime(year = today.year, month = 3, day = 1).date()
            
            # Move those who had BD this year to a next year
            if (date_this_year < today):
                date_this_year = date_this_year.replace(year = today.year + 1)
            
            # Move weekenders to MON
            if (date_this_year.weekday() >= 5):
                date_this_year += timedelta(days = 7 - date_this_year.weekday()) # Move 1 or 2 days forward
            
            if ((date_this_year - today).days <= 7):
                #congratulations
                result_set.append({"name":user.name, "congratulation_date":datetime.strftime(date_this_year, "%d.%m.%Y")})
        return result_set


    def save_data(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def load_data(filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено