import socket
from flask import Flask, request, jsonify, render_template
from manage3 import Library
from datetime import datetime

app = Flask(__name__)
library = Library()

# Admin password
ADMIN_PASSWORD = "Connect123"  # Nice secure password

def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def get_books():
    books_list = [book.to_dict() for book in library.books]
    return jsonify(books_list)

@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.json
    password = data.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"status": "failed", "message": "Unauthorized"})
    library.add_book(data["title"], data["author"], data["lang"], data["genre"])
    return jsonify({"status": "success"})

@app.route("/take_book", methods=["POST"])
def take_book():
    data = request.json
    title = data["title"]
    borrower_name = data.get("borrower_name", "Unknown")
    borrower_mobile = data.get("borrower_mobile", "Unknown")
    for book in library.books:
        if book.title.lower() == title.lower() and not book.is_taken:
            book.is_taken = True
            book.borrower_name = borrower_name
            book.borrower_mobile = borrower_mobile
            book.taken_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            book.submitted_date = None
            library.save_books()
            return jsonify({"status": "success"})
    return jsonify({"status": "failed", "message": "Book not available or already taken"})

@app.route("/submit_book", methods=["POST"])
def submit_book():
    data = request.json
    title = data["title"]
    for book in library.books:
        if book.title.lower() == title.lower() and book.is_taken:
            book.is_taken = False
            book.borrower_name = None
            book.borrower_mobile = None
            book.submitted_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            book.taken_date = None
            library.save_books()
            return jsonify({"status": "success"})
    return jsonify({"status": "failed", "message": "Book was not taken"})

@app.route("/delete_book", methods=["POST"])
def delete_book():
    data = request.json
    password = data.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"status": "failed", "message": "Unauthorized"})
    title = data["title"]
    for book in library.books:
        if book.title.lower() == title.lower():
            library.books.remove(book)
            library.save_books()
            return jsonify({"status": "success"})
    return jsonify({"status": "failed", "message": "Book not found"})

if __name__ == "__main__":
    free_port = find_free_port()
    print(f"Running on http://127.0.0.1:{free_port}")
    app.run(debug=True, port=free_port)
