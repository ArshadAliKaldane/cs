import os, requests
from datetime import datetime
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"11Qremn25PdgdFozxaLiCA","isbns":"1632168146,1416949658"})

# Check for environment variable
DB_ENV = os.getenv("DATABASE_URL")
# postgres://mdawjxjrukiihq:168f7846a9a3cb874316b3c6a733a986dbbc43347294851f3fea92638a75fd2e@ec2-54-152-40-168.compute-1.amazonaws.com:5432/d3h0dc84fv7d7r
if not DB_ENV:
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DB_ENV)
db = scoped_session(sessionmaker(bind=engine))

def apology(message, code=400):
    return render_template("apology.html", message=message), code

@app.route("/")
def index():
    """ main page """
    if session.get("user") is None:
        return redirect("/login")
    else:
        return render_template("index.html", user=session["user"].capitalize())

@app.route("/search", methods=["GET", "POST"])
def search():
    """ search for the books """
    if request.method == "GET":
        return redirect("/")
    search = request.form.get("search")
    if not search:
        return apology("please enter something", 403)
    search = "%" + search.lower() + "%"
    books = db.execute("SELECT * FROM books WHERE lower(title) LIKE :search OR lower(author) LIKE :search OR lower(isbn) LIKE :search", {"search":search}).fetchall()
    if not books:
        return apology("books not found. please try again with different name", 403)
    else:
        if session.get("user"):
            return render_template("index.html", books=books, user=session.get("user").capitalize(), result=len(books))
        else:
            return render_template("index.html", books=books, result=len(books))

@app.route("/author/<string:name>")
def author(name):
    """ books by specific author """
    books = db.execute("SELECT * FROM books where author=:author", {"author":name}).fetchall()
    if session.get("user"):
        return render_template("index.html", books=books, user=session["user"].capitalize(), result=len(books))
    else:
        return render_template("index.html", books=books, result=len(books))
'''
def get_api(book_isbn):
    KEY = "11Qremn25PdgdFozxaLiCA"
    return requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":KEY,"isbns":book_isbn})
'''
@app.route("/book/<string:book_isbn>")
def book(book_isbn):
    """ display book information """
    book = db.execute("SELECT * FROM books WHERE isbn=:book_isbn", {"book_isbn":book_isbn}).fetchone()
    if not book:
        return apology("no book found", 403)
    reviews = get_reviews(book_isbn)
    '''
    res = get_api(book_isbn)
    data = res.json()
    rating_count = data["books"][0]["work_ratings_count"]
    avg_rating = data["books"][0]["average_rating"]
    '''
    #avg_rating = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = '2'").fetchone()
    #rating_count = db.execute("SELECT COUNT(id) FROM reviews WHERE book_id = '2'").fetchone()
    return render_template("book.html", book=book, reviews=reviews)#, count=rating_count, rating=avg_rating)

def get_reviews(book_isbn):
    """ get book reviews from api """
    return db.execute("SELECT * FROM reviews JOIN users ON reviews.book_id=(SELECT id FROM books WHERE isbn=:isbn) where users.id=reviews.user_id ORDER BY date DESC",
            {"isbn":book_isbn}).fetchall()

@app.route("/book/review/<string:book_isbn>", methods=["POST"])
def review(book_isbn):
    """ review the book once per user """
    rating = request.form.get("rating")
    message = request.form.get("message")
    if session.get("user_id"):
        if not message:
            return apology("you must type something for review", 403)
        book = db.execute("SELECT * FROM books WHERE isbn=:book_isbn", {"book_isbn":book_isbn}).fetchone()
        reviews = get_reviews(book_isbn)
        # allow only one review per user
        for rev in reviews:
            if rev["name"] == session["user"]:
                if rev["message"]:
                    return apology("you can not review more than once.", 403)
        db.execute("INSERT INTO reviews(message, rating, user_id, book_id, date) VALUES (:message, :rating, :user_id, :book_id, :date)",
                {"message":message, "rating":rating, "user_id":session["user_id"], "book_id":book["id"], "date":datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        db.commit()
        return render_template("book.html", book=book, reviews=get_reviews(book_isbn))
    else:
        return apology("you must be logged in to review a book", 403)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ login """
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # get values from login from
        name = request.form.get("name")
        password = request.form.get("password")

        # make sure name & pass is not empty
        if not name:
            return apology("username cannot be empty!", 403)
        elif not password:
            return apology("password cannot be empty!", 403)

        # make sure username and password are correct
        user = db.execute("SELECT * FROM users WHERE name=:name",{"name":name}).fetchone()
        if not user:
            return apology("user doesn't exists!", 403)
        elif name == user["name"] and password == user["password"]:
            session["user"] = user["name"]
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return apology("invalid username or password.", 403)

@app.route("/logout")
def logout():
    """ logout """
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ register new user """
    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    else:
        # get values from register from
        name = request.form.get("name")
        password = request.form.get("password")

        # make sure name & pass is not empty
        if not name:
            return apology("username cannot be empty!", 403)
        elif not password:
            return apology("password cannot be empty!", 403)

        # do not allow repeated username
        row = db.execute("SELECT * FROM users WHERE name=:name",{"name":name}).fetchall()
        
        if row and row[0]["name"] == name:
            return apology("Sorry, username already exists! Try again with another username.", 403)
        else:    
            # register a new user
            db.execute("INSERT INTO users(name, password) VALUES (:name, :pass)", {"name":name, "pass":password})
            db.commit()
            session["user"] = name
            session["user_id"] = row[0]["id"]
            return redirect("/")

@app.route("/api/<string:book_isbn>")
def api(book_isbn):
    """ provide our own api """
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":book_isbn}).fetchone()
    if not book:
        return jsonify({"error":"no book found"})
    #res = get_api(book_isbn)
    #data = res.json()
    return jsonify({
        "title": book["title"],
        "author": book["author"],
        "year": int(book["year"]),
        "isbn": book["isbn"],
        #"review_count": data["books"][0]["work_ratings_count"],
        #"average_rating": float(data["books"][0]["average_rating"])
    })

@app.route("/isbn")
def isbn():
    isbn = db.execute("SELECT isbn from books ORDER BY id LIMIT 1000").fetchall()
    f = open('isbn.txt','a')
    for x in isbn:
        f.write(x['isbn']+'\n')
    f.close()
    return render_template('isbn.html',isbns=isbn)