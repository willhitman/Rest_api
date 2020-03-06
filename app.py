from flask import Flask,request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy #install using 'pip insatall flask_sqlalchemy' command
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
import jwt   #need to install via the 'pip install jwt' command on terminal
import datetime
from functools import wraps

app = Flask(__name__)
 
app.config["SECRET_KEY"]= 'itsprollyforthebest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'

db = SQLAlchemy(app)


#authentication for any route except logging in
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
    #end of authentication route

#this route is for logging in the site
@app.route('/login',methods = ['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('ENTER USERNAME AND PASSWORD TO CONTINUE', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
    user = User.query.filter_by(user_name = auth.username).first()

    if not user:
        return make_response('USERNAME OR PASSWORD INCORRECT1', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})
        
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('USERNAME OR PASSWORD INCORRECT2', 401, {'WWW-Authenticate' : 'Basic realm = "Login required"'})


#this route is for creating a new user

#.................... ................. ...................... .................. .................. ........................ ................................ ...................................... .................
@app.route('/user', methods = ['POST'])#ADDING A NEW USER HERE
#@token_required
def add_new_user():
    #if not current_user.admin:
        #return jsonify({"message": "Not authorized"})
        
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(user_id = str(uuid4()), user_name = data ['user_name'], password = hashed_password, admin = False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user added successfully'})

#.................... .......................... ..................... ..................... ................... ........................... ........................
from addmin_routes import *
from user_routes import *
from bus_routes import *

if __name__ == '__main__':
    app.run(debug = True)