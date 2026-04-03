"""User-related functions: authentication, profile images, and user reviews."""

from werkzeug.security import check_password_hash, generate_password_hash
import db


def get_user(user_id):
    """Return user data for a given user ID, including whether the user has an image."""
    sql = """SELECT id, username, image IS NOT NULL has_image FROM users WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_image(user_id):
    """Return the image data for a given user ID, or None if no image exists."""
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0]["image"] if result and result[0]["image"] else None


def get_reviews(user_id):
    """Return all reviews authored by the specified user, ordered by newest first."""
    sql = """SELECT id, title FROM reviews WHERE user_id = ? ORDER BY id DESC"""
    return db.query(sql, [user_id])


def create_user(username, password):
    """Create a new user with a hashed password."""
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    """Check if login credentials are valid. Return user ID if valid, None otherwise."""
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None


def update_image(user_id, image):
    """Update the profile image for the specified user."""
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])
