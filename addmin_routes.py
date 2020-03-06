
from app import *
from app import token_required
from model import *

#GETTING ALL THE USERS
@app.route('/user', methods = ['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    result = []
    for user in users:
        user_info = {}
        user_info['id'] = user.user_id
        user_info['name'] = user.user_name
        user_info['password'] = user.password
       
        result.append(user_info)
    return jsonify({"users" : result })


#GETTING A SINGLE USER 
@app.route('/user/<user_id>', methods = ['GET'])
@token_required
def get_single_user(current_user, user_id):
    #if not current_user.admin:
        #return jsonify({"message": "Not authorized"})
        

    user = User.query.filter_by(user_id = user_id).first()#only get the first result because the user_id is unique
    
    if not user:
        return jsonify({"message" : 'No user found'})
    user_data = {}
    user_data["user_id"] = user.user_id
    user_data["user_name"] = user.user_name
    user_data["password"] = user.password
    
    
    return jsonify({"user" : user_data})

#end*********************************************************************************************
'''
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

    lets just do away with this route for now!!
    '''
    

