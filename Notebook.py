from datetime import datetime, timedelta
from collections import UserDict
from src.models import *
import pickle

class Note:
    def __init__(self, note: str, tags=None):
        self.note = note
        self.tags = tags if tags else []

class Notebook(UserDict):
    def add_note(self, note: Note):
        key = len(self.data) + 1  # Простой числовой ключ для каждой заметки
        self.data[key] = note

    def find_note(self, query: str):
        result_set = []
        for key, note in self.data.items():
            if query.lower() in note.note.lower() or any(query.lower() in tag.lower() for tag in note.tags):
                result_set.append({"note_id": key, "note": note.note, "tags": note.tags})
        return result_set
    
    def delete_note(self, note_id: int):
        if note_id not in self.data:
            raise KeyError("Note doesn't exist")
        self.data.pop(note_id)

    def save_data(self, filename="notebook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_data(filename="notebook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return Notebook()  # Повернення нової записної книги, якщо файл не знайдено