from app import *
from app import token_required
from model import *



@app.route('/user_bus', methods = ['POST'])
#no need for authentication.....will ad email or phone verification later on
def add_new_bus_user():           
    
    data = request.get_json()
    
    print(data, file=sys.stderr)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Bus(Bus_id = str(uuid4()), Bus_name = data['user_name'], Bus_pass = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'New user added successfully'})
#..................        .. .......................... ..................... ..................... ................... ........................... ........................


@app.route('/foo_outlets', methods =['POST','GET'])
@token_required
def get_food(current_user):
    temp = Bus_data.query.all()
    all_data['business'] = Bus.query.filter_by(Bus_id = temp.Bus_id).first()
    all_data['address'] = temp.address
    all.data['type']= temp.typ
    return jsonify({"message":all_data})