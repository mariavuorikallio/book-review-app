"""Review-related functions: managing reviews, comments, and classes."""

import db


def get_all_classes():
    """Return all classes and their possible values as a dictionary {title: [values]}."""
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes


def add_review(title, author, description, user_id, classes):
    """Add a new review with associated classes."""
    sql = """INSERT INTO reviews (title, author, description, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, author, description, user_id])

    review_id = db.last_insert_id()

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [review_id, class_title, class_value])


def add_comment(review_id, user_id, content):
    """Add a comment to a review."""
    db.execute(
        "INSERT INTO comments (review_id, user_id, content) VALUES (?, ?, ?)",
        [review_id, user_id, content]
    )

    sql = "SELECT user_id, title FROM reviews WHERE id = ?"
    review = db.query(sql, [review_id])[0]

    if review["user_id"] != user_id:
        message = f"Uusi kommentti arvosteluusi: {review['title']}"
        add_notification(review["user_id"], review_id, message)

def get_notifications(user_id):
    """Return unread notifications for a user."""
    sql = """
        SELECT notifications.id,
               notifications.review_id,
               notifications.message,
               notifications.created_at,
               notifications.seen,
               reviews.title
        FROM notifications
        JOIN reviews ON notifications.review_id = reviews.id
        WHERE notifications.user_id = ? AND notifications.seen = 0
        ORDER BY notifications.created_at DESC
    """
    return db.query(sql, [user_id])

def add_notification(user_id, review_id, message):
    """Create a new notification."""
    sql = """
        INSERT INTO notifications (user_id, review_id, message)
        VALUES (?, ?, ?)
    """
    db.execute(sql, [user_id, review_id, message])

def mark_notification_seen(notification_id):
    """Mark notification as seen."""
    sql = "UPDATE notifications SET seen = 1 WHERE id = ?"
    db.execute(sql, [notification_id])

def get_comments(review_id):
    """Return all comments for a review, including user information, ordered by newest first."""
    sql = """SELECT users.id AS user_id, users.username, comments.content, comments.created_at
             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.review_id = ?
             ORDER BY comments.created_at DESC"""
    return db.query(sql, [review_id])


def get_classes(review_id):
    """Return all class entries for a specific review."""
    sql = "SELECT title, value FROM review_classes WHERE review_id = ?"
    return db.query(sql, [review_id])


def get_reviews():
    """Return all reviews with their ID and title, ordered by newest first."""
    sql = "SELECT id, title FROM reviews ORDER BY id DESC"
    return db.query(sql)


def get_review(review_id):
    """Return full information for a single review, including author data."""
    sql = """SELECT reviews.id,
                    reviews.title,
                    reviews.author,
                    reviews.description,
                    users.id AS user_id,
                    users.username
             FROM reviews
             JOIN users ON reviews.user_id = users.id
             WHERE reviews.id = ?"""
    result = db.query(sql, [review_id])
    return result[0] if result else None


def update_review(review_id, title, author, description, classes):
    """Update a review and its associated classes."""
    sql = """UPDATE reviews
             SET title = ?,
                 author = ?,
                 description = ?
             WHERE id = ?"""
    db.execute(sql, [title, author, description, review_id])

    sql = "DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "INSERT INTO review_classes (review_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [review_id, class_title, class_value])

def remove_review(review_id):
    """Delete a review and all related data."""
    sql = "DELETE FROM comments WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "DELETE FROM notifications WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])


def find_reviews(query):
    """Search for reviews by title, author, or description containing the query string."""
    sql = """SELECT id, title
             FROM reviews
             WHERE title LIKE ? OR author LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])
