import json
import os

class Book:
    def __init__(self, title, author, lang, genre):
        self.title = title
        self.author = author
        self.lang = lang
        self.genre = genre
        self.is_taken = False
        self.borrower_name = None
        self.borrower_mobile = None
        self.taken_date = None
        self.submitted_date = None

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "lang": self.lang,
            "genre": self.genre,
            "is_taken": self.is_taken,
            "borrower_name": self.borrower_name,
            "borrower_mobile": self.borrower_mobile,
            "taken_date": self.taken_date,
            "submitted_date": self.submitted_date
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["lang"], data["genre"])
        book.is_taken = data.get("is_taken", False)
        book.borrower_name = data.get("borrower_name")
        book.borrower_mobile = data.get("borrower_mobile")
        book.taken_date = data.get("taken_date")
        book.submitted_date = data.get("submitted_date")
        return book


class Library:
    def __init__(self, storage_file="books.json"):
        self.storage_file = storage_file
        self.books = []
        self.load_books()

    def add_book(self, title, author, lang, genre):
        new_book = Book(title, author, lang, genre)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, title):
        self.books = [book for book in self.books if book.title.lower() != title.lower()]
        self.save_books()

    def save_books(self):
        with open(self.storage_file, "w") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def load_books(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                try:
                    data = json.load(f)
                    self.books = [Book.from_dict(book) for book in data]
                except json.JSONDecodeError:
                    self.books = []
