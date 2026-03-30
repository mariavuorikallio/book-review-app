import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import reviews

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)
    
@app.route("/find_review")
def find_review():
    query = request.args.get("query")
    if query:
       results = reviews.find_reviews(query)
    else:
       query = ""
       results = []
    return render_template("find_review.html", query=query, results=results)
    
@app.route("/review/<int:review_id>")
def show_review(review_id):
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    return render_template("show_review.html", review=review)
    
@app.route("/new_review")
def new_review():
    require_login()
    return render_template("new_review.html")
    
@app.route("/create_review", methods=["POST"])
def create_review():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
       abort(403)
    author = request.form["author"]
    if not author or len(author) > 50:
       abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
       abort(403)
    user_id = session["user_id"]
    
    reviews.add_review(title, author, description, user_id)
    
    return redirect("/")

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    if review["user_id"] != session["user_id"]:
       abort(403)
    return render_template("edit_review.html", review=review)
    
@app.route("/update_review", methods=["POST"])
def update_review():
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    if review["user_id"] != session["user_id"]:
       abort(403)
    title = request.form["title"]
    author = request.form["author"]
    description = request.form["description"]
    
    reviews.update_review(review_id, title, author, description)
    
    return redirect("/review/" + str(review_id))
    
@app.route("/remove_review/<int:review_id>", methods=["POST", "GET"])
def remove_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    if review["user_id"] != session["user_id"]:
       abort(403)
    if request.method == "GET":
       return render_template("remove_review.html", review=review)
    if request.method == "POST":
       if "remove" in request.form:
           reviews.remove_review(review_id)
           return redirect("/")
       else:
           return redirect("/review/" + str(review_id))
    
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
       return render_template("login.html")
       
    if request.method == "POST":
       username = request.form["username"]
       password = request.form["password"]
       
       sql = "SELECT id, password_hash FROM users WHERE username = ?"
       result = db.query(sql, [username])[0]
       user_id = result["id"]
       password_hash = result["password_hash"]
       
       if check_password_hash(password_hash, password):
          session["user_id"] = user_id
          session["username"] = username
          return redirect("/")
       else:
          return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
