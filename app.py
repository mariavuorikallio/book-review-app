import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import reviews
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)
    
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
       abort(404)
    reviews = users.get_reviews(user_id)
    return render_template("show_user.html", user=user, reviews=reviews)
    
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
    print(review)
    if not review:
       abort(404)
    classes = reviews.get_classes(review_id)
    comments = reviews.get_comments(review_id)
    return render_template("show_review.html", review=review, classes=classes, comments=comments)
    
@app.route("/new_review")
def new_review():
    require_login()
    classes = reviews.get_all_classes()
    return render_template("new_review.html", classes=classes)
       
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
    
    all_classes = reviews.get_all_classes()
    
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
           class_title, class_value = entry.split(":")
           if class_title not in all_classes:
              abort(403)
           if class_value not in all_classes[class_title]:
              abort(403)
           classes.append((class_title, class_value))
           
    reviews.add_review(title, author, description, user_id, classes)
    
    return redirect("/")
    
@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review:
       abort(403)
    user_id = session["user_id"]
    content = request.form["content"] 
    if not content or len(content) > 1000:
        abort(403)
    reviews.add_comment(review_id, user_id, content)
    
    return redirect("/review/" + str(review_id))

@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    require_login()
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    if review["user_id"] != session["user_id"]:
       abort(403)
    all_classes = reviews.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in reviews.get_classes(review_id):
        classes[entry["title"]] = entry["value"]
    return render_template("edit_review.html", review=review, classes=classes, all_classes=all_classes)
    
@app.route("/update_review", methods=["POST"])
def update_review():
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review:
       abort(404)
    if review["user_id"] != session["user_id"]:
       abort(403)
    title = request.form["title"]
    if not title or len(title) > 50:
       abort(403)
    author = request.form["author"]
    if not author or len(author) > 50:
       abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
       abort(403)
    
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
           class_title, class_value = entry.split(":")
           if class_title not in all_classes:
              abort(403)
           if class_value not in all_classes[class_title]:
              abort(403)
           classes.append((class_title, class_value))       
           
    reviews.update_review(review_id, title, author, description, classes)
    
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
    
    try:
       users.create_user(username, password1)
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
       user_id = users.check_login(username, password)
       if user_id:
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
