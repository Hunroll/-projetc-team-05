from collections import UserDict
from typing import List

from src.models import Note


class NoteBook(UserDict):
    """Class for managing notes, inherited from UserDict.
    Supported operations:
        - add_note(title: str, content: str) -> str
        - edit_note(title: str, new_content: str) -> str
        - delete_note(title: str) -> str
        - search_notes(keyword: str) -> str
            searches for notes by keyword in the content. partial match non-case-sensitive
        - show_all_notes() -> str
        - add_tags_to_note(title: str, tags: List[str]) -> str
        - remove_tag_from_note(title: str, tag: str) -> str
        - search_notes_by_tags(tags: List[str]) -> str
            searches for notes by tags. full match required
    """
    def __init__(self):
        super().__init__()

    def add_note(self, title: str, content: str) -> str:
        if title in self.data:
            return "Note with this title already exists."
        self.data[title] = Note(title, content)
        return f"Note '{title}' added successfully."

    def edit_note(self, title: str, new_content: str) -> str:
        if title not in self.data:
            return "Note not found."
        self.data[title].edit_content(new_content)
        return f"Note '{title}' edited successfully."

    def delete_note(self, title: str) -> str:
        if title not in self.data:
            return "Note not found."
        del self.data[title]
        return f"Note '{title}' deleted successfully."

    def search_notes(self, keyword: str) -> str:
        found_notes = {title: note for title, note in self.data.items() if note.search_by_keyword(keyword)}
        if not found_notes:
            return "No notes found."
        return "\n".join([str(note) for note in found_notes.values()])

    def show_all_notes(self) -> str:
        if not self.data:
            return "No notes available."
        # TODO: prettify output
        result_str = "{:<20} {:<20} {:<20}\n".format("Title", "Content", "Tags")
        for k, note in self.data.items():
            result_str += "{:<20} {:<20} {:<20}\n".format(
                str(note.title), 
                str(note.content),
                str(note.tags))
        return result_str
    
    def add_tags_to_note(self, title: str, tags: List[str]) -> str:
        if title not in self.data:
            return "Note not found."
        for tag in tags:
            self.data[title].add_tag(tag)
        return f"Tags '{', '.join(tags)}' added to note '{title}'."

    def remove_tag_from_note(self, title: str, tag: str) -> str:
        if title not in self.data:
            return "Note not found."
        self.data[title].remove_tag(tag)
        return f"Tag '{tag}' removed from note '{title}'."

    def search_notes_by_tags(self, tags: List[str]) -> str:
        found_notes = {
            title: note for title, note in self.data.items()
            if all(tag in note.tags.value for tag in tags)
        }
        if not found_notes:
            return f"No notes found with tags {', '.join(tags)}."
        # TODO: prettify output
        result_str = "{:<20} {:<20} {:<20}\n".format("Title", "Content", "Tags")
        for k, note in found_notes.items():
            result_str += "{:<20} {:<20} {:<20}\n".format(
                str(note.title), 
                str(note.content),
                str(note.tags))
        return result_str
