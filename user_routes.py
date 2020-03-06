
from app import app
from model import *

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
