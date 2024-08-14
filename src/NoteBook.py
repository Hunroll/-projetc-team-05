# src/NoteBook.py
class NoteBook:
    def __init__(self):
        self.notes = {}

    def add_note(self, title, content):
        if title in self.notes:
            return "Note with this title already exists."
        self.notes[title] = content
        return f"Note '{title}' added successfully."

    def edit_note(self, title, new_content):
        if title not in self.notes:
            return "Note not found."
        self.notes[title] = new_content
        return f"Note '{title}' edited successfully."

    def delete_note(self, title):
        if title not in self.notes:
            return "Note not found."
        del self.notes[title]
        return f"Note '{title}' deleted successfully."

    def search_notes(self, keyword):
        found_notes = {title: content for title, content in self.notes.items() if keyword in title or keyword in content}
        if not found_notes:
            return "No notes found."
        return "\n".join([f"{title}: {content}" for title, content in found_notes.items()])

    def show_all_notes(self):
        if not self.notes:
            return "No notes available."
        return "\n".join([f"{title}: {content}" for title, content in self.notes.items()])
