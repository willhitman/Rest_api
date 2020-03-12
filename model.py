from app import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80), unique = True)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80))
    body = db.Column(db.String(100))
    seen = db.Column(db.Integer)
    count = db.Column(db.Integer)
    post_image = db.Column(db.Boolean)

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Bus_id = db.Column(db.String(80))
    Bus_name = db.Column(db.String(100))
    Bus_pass = db.Column(db.String(100))

class Bus_data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Bus_id = db.Column(db.String(80), unique = True)
    address = db.Column(db.String(150))
    Tax_F_N = db.Column(db.String(300))
    typ = db.Column(db.String(100))

class Bus_Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Bus_id = db.Column(db.String(80))
    post_text = db.Column(db.String(150))
    post_image = db.Column(db.Boolean)

class Bus_cat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Bus_id = db.Column(db.String(80))
    Cost = db.Column(db.Numeric)
    image = db.Column(db.String(3000))
    descrip = db.Column(db.String(200))

class User_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(30), unique = True)
    image = db.Column(db.String(500))

class Posts_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Post_id = db.Column(db.Integer, unique = True)
    image = db.Column(db.String(3000))

#this is strictly for future use but willH180300N use it only in testing and development
class Add_image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    add_id = db.Column(db.String(30), unique = True)
    image = db.Column(db.String(3000))

