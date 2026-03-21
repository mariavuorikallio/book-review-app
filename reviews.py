import db

def new_review(title, author, description, user_id):
    sql = """INSERT INTO reviews (title, author, description, user_id) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, author, description, user_id])
    
