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

class User_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(30), unique = True)
    image = db.Column(db.String(3000))

class Posts_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Post_id = db.Column(db.Integer, unique = True)
    image = db.Column(db.String(3000))

#this is strictly for future use but will use it only in testing and development
class Add_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    add_id = db.Column(db.String(30))
    image = db.Column(db.String(3000))

