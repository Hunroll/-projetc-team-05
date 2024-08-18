from collections import UserDict
from datetime import timedelta
from typing import Dict

from ccnb.src.models import *


class AddressBook(UserDict):
    """Address book class
        data: dict with key: int, value: UserRecord
        user_id: int, autoincrement id for new records
        supported operations:
            - add_record(record: UserRecord):
                validates if record already exists
            - find(name: str) -> UserRecord|None
            - search(pattern: str) -> List[UserRecord]:
                search for a record by pattern in all fields
                search order: name, phone, birthday, email, address
                non-case-sensitive search
            - delete(name: str)
            - get_upcoming_birthdays(specific_date = None, days = 7) -> List[Dict[str, str]]
                returns a list of upcoming birthdays within a days range (default 7) from a specific date (default today)
                specific_date: str, format: "dd.mm.yyyy"
                days: int, number of days to look ahead
    """
    def __init__(self):
        super().__init__()

    def add_record(self, record: UserRecord):
        key = max(self.data.keys()) + 1 if self.data.keys() else 1 
        if key in self.data:
            raise KeyError("Contact already exists")
        self.data[key] = record

    def find(self, name: str) -> UserRecord|None:
        for key in self.data:
            if name.lower() == self.data[key].name.value.lower():
                return self.data[key]
        return None

    def search(self, pattern: str) -> List[UserRecord]:
        result = []
        for key in self.data:
            if self.data[key].name and pattern.lower() in self.data[key].name.value.lower():
                result.append(self.data[key])
            elif self.data[key].phones and any(pattern in phone for phone in self.data[key].phones):
                result.append(self.data[key])
            elif self.data[key].birthday and pattern in str(self.data[key].birthday.value):
                result.append(self.data[key])
            elif self.data[key].emails and any(pattern.lower() in email.lower() for email in self.data[key].emails):
                result.append(self.data[key])
            elif self.data[key].address and pattern.lower() in self.data[key].address.value.lower():
                result.append(self.data[key])
        return result

    def delete(self, name: str):
        contact = self.find(name)
        if not contact:
            raise KeyError("Contact doesn\'t exist")
        self.data = dict((key, val) for (key, val) in self.data.items() if val != contact)

    def get_upcoming_birthdays(self, specific_date = None, days = 7) -> List[Dict[str, str]]:
        congrats_list = []
        today = datetime.strptime(specific_date, "%d.%m.%Y").date() if specific_date is not None else datetime.today().date()
        users_with_bd = list(v for (k, v) in self.data.items() if v.birthday)
        for user in users_with_bd:
            original_date = user.birthday.value.date()
            
            # Get this year's date
            try:
                date_this_year = original_date.replace(year = today.year)
            except:
                # TODO: Remove this after adding validation for birthdays at 02/29
                #29th of Feb
                date_this_year = datetime(year = today.year, month = 3, day = 1).date()
            
            # Move those who had BD this year to a next year
            if date_this_year < today:
                date_this_year = date_this_year.replace(year = today.year + 1)
            
            # Move weekenders to MON
            if date_this_year.weekday() >= 5:
                date_this_year += timedelta(days = 7 - date_this_year.weekday()) # Move 1 or 2 days forward
            
            if (date_this_year - today).days <= days:
                #congratulations
                congrats_list.append({"name":user.name, "congratulation_date":datetime.strftime(date_this_year, "%d.%m.%Y")})
        return congrats_list

   