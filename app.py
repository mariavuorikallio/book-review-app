"""Main Flask application for handling reviews and user accounts."""

import secrets
import sqlite3

from flask import Flask, abort, flash, redirect, render_template, request, session, make_response

import config
import reviews
import users

app = Flask(__name__)
app.secret_key = config.secret_key


def check_csrf():
    """Check if CSRF token in session matches the one in form."""
    if "csrf_token" not in session or request.form.get("csrf_token") != session["csrf_token"]:
        abort(403)


def require_login():
    """Ensure that a user is logged in."""
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    """Render the home page with all reviews."""
    all_reviews = reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show a user's profile and their reviews."""
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_reviews = users.get_reviews(user_id)
    return render_template("show_user.html", user=user, reviews=user_reviews)


@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    """Allow a logged-in user to add a profile image."""
    require_login()
    if request.method == "GET":
        return render_template("add_image.html")
    check_csrf()
    file = request.files.get("file")
    if not file or not file.filename.endswith(".jpg"):
        return "VIRHE: väärä tiedostomuoto"
    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"
    user_id = session["user_id"]
    users.update_image(user_id, image)
    return redirect(f"/user/{user_id}")


@app.route("/image/<int:user_id>")
def show_image(user_id):
    """Return the user's profile image as a JPEG response."""
    image = users.get_image(user_id)
    if not image:
        abort(404)
    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/find_review")
def find_review():
    """Search reviews by query string."""
    query = request.args.get("query")
    if query:
        results = reviews.find_reviews(query)
    else:
        query = ""
        results = []
    return render_template("find_review.html", query=query, results=results)


@app.route("/review/<int:review_id>")
def show_review(review_id):
    """Display a specific review with its classes and comments."""
    review = reviews.get_review(review_id)
    if not review:
        abort(404)
    classes = reviews.get_classes(review_id)
    comments = reviews.get_comments(review_id)
    return render_template(
        "show_review.html", review=review, classes=classes, comments=comments
    )


@app.route("/new_review")
def new_review():
    """Render the form to create a new review."""
    require_login()
    classes = reviews.get_all_classes()
    return render_template("new_review.html", classes=classes)


@app.route("/create_review", methods=["POST"])
def create_review():
    """Create a new review with form data and selected classes."""
    require_login()
    check_csrf()
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
            if class_title not in all_classes or class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    reviews.add_review(title, author, description, user_id, classes)
    return redirect("/")


@app.route("/create_comment", methods=["POST"])
def create_comment():
    """Add a comment to a review."""
    require_login()
    check_csrf()
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review:
        abort(403)
    user_id = session["user_id"]
    content = request.form["content"]
    if not content or len(content) > 1000:
        abort(403)
    reviews.add_comment(review_id, user_id, content)
    return redirect(f"/review/{review_id}")


@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    """Render the edit page for a review."""
    require_login()
    review = reviews.get_review(review_id)
    if not review or review["user_id"] != session["user_id"]:
        abort(404)
    all_classes = reviews.get_all_classes()
    classes = {my_class: "" for my_class in all_classes}
    for entry in reviews.get_classes(review_id):
        classes[entry["title"]] = entry["value"]
    return render_template(
        "edit_review.html", review=review, classes=classes, all_classes=all_classes
    )


@app.route("/update_review", methods=["POST"])
def update_review():
    """Update an existing review with new form data."""
    require_login()
    check_csrf()
    review_id = request.form["review_id"]
    review = reviews.get_review(review_id)
    if not review or review["user_id"] != session["user_id"]:
        abort(404)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    author = request.form["author"]
    if not author or len(author) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    all_classes = reviews.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes or class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
    reviews.update_review(review_id, title, author, description, classes)
    return redirect(f"/review/{review_id}")


@app.route("/remove_review/<int:review_id>", methods=["POST", "GET"])
def remove_review(review_id):
    """Delete a review after confirmation."""
    require_login()
    review = reviews.get_review(review_id)
    if not review or review["user_id"] != session["user_id"]:
        abort(404)
    if request.method == "GET":
        return render_template("remove_review.html", review=review)
    check_csrf()
    if "remove" in request.form:
        reviews.remove_review(review_id)
        return redirect("/")
    return redirect(f"/review/{review_id}")


@app.route("/register")
def register():
    """Render the user registration page."""
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    """Create a new user with username and password."""
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    flash("Tunnus luotu")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login, set session and CSRF token."""
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    """Log out the current user."""
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
