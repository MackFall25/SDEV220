from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DB config (SQLite file in this folder, like in the video) ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Model (Book with id, book_name, author, publisher) ---
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        # mirrors the video’s __repr__ style: useful in the shell
        return f"{self.book_name} - {self.author} ({self.publisher})"

#  Hello route 
@app.route("/")
def hello():
    return "Hello"

# GET /books: list all 
@app.route("/books")
def get_books():
    books = Book.query.all()
    output = []
    for b in books:
        book_data = {
            "id": b.id,
            "book_name": b.book_name,
            "author": b.author,
            "publisher": b.publisher,
        }
        output.append(book_data)
    return jsonify({"items": output})

# GET /books/<id>: fetch one 
@app.route("/books/<int:book_id>")
def get_book(book_id):
    b = Book.query.get_or_404(book_id)
    return jsonify({
        "id": b.id,
        "book_name": b.book_name,
        "author": b.author,
        "publisher": b.publisher,
    })

# POST /books: create one 
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json(force=True)  
    b = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id}), 201


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    b = Book.query.get(book_id)
    if b is None:
        return jsonify({"error": "not found"}), 404
    db.session.delete(b)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
