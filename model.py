from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80), unique = True)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
   

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    body = db.Column(db.String(100))
    seen = db.Column(db.Boolean)
    count = db.Column(db.Integer)