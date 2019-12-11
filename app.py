from flask import Flask,request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

app.config["SECRET_KEY"]= 'itsprollyforthebest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.String(80), unique = True)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    body = db.Column(db.String(100))
    seen = db.Column(db.Boolean)
    count = db.Column(db.Integer)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x.access-token' in request.headers:
            token = request.headers['x.access-token']

        if not token:
            return jsonify({"message" : "Token is mising"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(user_id = data['user_id']).first()
        except:
            return jsonify({"message" : "Token is invalid"}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated
#.....start of admistrative routes.......
@app.route('/user', methods = ['GET'])#GETTING ALL THE USERS
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "Not authorized"})

    users = User.query.all()
    result = []
    for user in users:
        user_info = {}
        user_info['id'] = user.user_id
        user_info['name'] = user.user_name
        user_info['password'] = user.password
        user_info['admin'] = user.admin
        result.append(user_info)
    return jsonify({"users" : result })

@app.route('/user/<user_id>', methods = ['GET'])#GETTING A SINGLE USER 
@token_required
def get_single_user(current_user, user_id):
    if not current_user.admin:
        return jsonify({"message": "Not authorized"})
        

    user = User.query.filter_by(user_id = user_id).first()#only get the first result because the user_id is unique
    
    if not user:
        return jsonify({"message" : 'No user found'})
    user_data = {}
    user_data["user_id"] = user.user_id
    user_data["user_name"] = user.user_name
    user_data["password"] = user.password
    user_data["admin"] = user.admin
    
    return jsonify({"user" : user_data})


@app.route('/user/<user_id>', methods = ['PUT'])#update user
@token_required
def update_user(current_user, user_id):

    if not current_user.admin:
        return jsonify({"message": "Not authorized"})
        

    user = User.query.filter_by(user_id = user_id).first()#only get the first result because the user_id is unique

    if not user:
        return jsonify({"message" : 'No user found'})
    if not user.admin == True:
        user.admin = True
    else:
        user.admin = False
        db.session.commit()

    return({"message" : "User updated"})

@app.route('/user', methods = ['POST'])#ADDING A NEW USER HERE
@token_required
def add_new_user(current_user):
    if not current_user.admin:
        return jsonify({"message": "Not authorized"})
        
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(user_id = str(uuid4()), user_name = data ['user_name'], password = hashed_password, admin = False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user added successfully'})

#end of admistrative routes

#this route is for everyone

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
    user = User.query.filter_by(user_name = auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
        
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})

#Start of end user routes
@app.route('/post', methods = ['POST','GET'])
@token_required
def post_something(current_user):
    if request.method == 'POST':
        post_data = request.get_json()
        
        new_post =Posts(user_id = current_user.user_id,body = post_data['text'],seen = False,count= "0")
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message" : "Post successfull"})
    
    #This is for getting all posts
    elif request.method == 'GET':
        posts = Posts.query.all()
        
        collected_posts = []
        for post in posts:
            all_posts = {}
            all_posts['id']=post.id
            all_posts['owner']=post.user_id
            all_posts['body'] = post.body
            all_posts['seen'] = post.seen
            all_posts['likes']=post.count
            collected_posts.append(all_posts)
    
        return jsonify({"message" : collected_posts})

@app.route("/post/<post_id>", methods = ['PUT','GET'])
@token_required
def get_by_post_id(current_user,post_id):

    if request.method == 'GET':
        single_post = Posts.query.filter_by(id=post_id).first()
        post_owner = User.query.filter_by(user_id = single_post.user_id).first()
        single = {}
        single['id'] = single_post.id
        single['owner'] = post_owner.user_name
        single['body'] = single_post.body

        if single_post.seen == False:
            single_post.seen = True
            db.session.commit()

        single['seen']=single_post.seen
        single['likes'] = single_post.count

        return jsonify({"post" : single})

    elif request.method == 'PUT':
        liked_post = Posts.query.filter_by(id=post_id).first()
        liked_post.count += 1
        db.session.commit()


        return jsonify({"message": "Post liked"})

#end of user routes.............................


if __name__ == '__main__':
    app.run(debug = True)