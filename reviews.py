import db

def add_review(title, author, description, user_id):
    sql = """INSERT INTO reviews (title, author, description, user_id) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, author, description, user_id])
    
def get_reviews():
    sql = "SELECT id, title FROM reviews ORDER BY id DESC"
    return db.query(sql)
    
def get_review(review_id):
    sql = """SELECT reviews.id,
                    reviews.title,
                    reviews.author,
                    reviews.description,
                    users.id user_id,
                    users.username
             FROM reviews, users
             WHERE reviews.user_id = users.id AND
                   reviews.id =?"""
    result = db.query(sql, [review_id])
    return result[0] if result else None

def update_review(review_id, title, author, description):
    sql = """UPDATE reviews 
             SET title = ?, 
                 author = ?, 
                 description = ? 
             WHERE id = ?"""
    db.execute(sql, [title, author, description, review_id])                           
     
def remove_review(review_id):
    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])  
    
def find_reviews(query):
    sql = """SELECT id, title
             FROM reviews
             WHERE title LIKE ? OR author LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like])                    
