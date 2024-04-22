#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from models import db, User, Friendship, Notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
api = Api(app)
bcrypt = Bcrypt(app)

#============ For Testing Purposes Only!!! ==================================#
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)

    def post(self):
        response = request.get_json()
        name = response["name"]

        #add username and password when you are working on it.
        #But, not now 4-10-24

        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 200)
        except:
            return make_response({"message": "Error, new user could not be made"}, 404)
    
class Friendships(Resource):
    def get(self):
        friendships = [friendship.to_dict() for friendship in Friendship.query.all()]
        return make_response(friendships, 200)
#============ For Testing Purposes Only!!! ==================================#

class SpecificUsers(Resource):
    def get(self, id):
        try:
            user = User.query.filter(User.id == id).first().to_dict()
            print(user)
            return make_response(user, 200)
        except:
            return make_response({"message": f"Could not find user with ID: {id}"}, 404)
        
    def post(self):
        pass

class FriendRequest(Resource):
    def post(self):
        response = request.get_json()
        requester_id = int(response["sender_id"])
        reciever_id = int(response["reciever_id"])

        try:
            requester = User.query.filter(User.id == requester_id).first()
            requester.send_friend_request(reciever_id)
            created_request = Friendship.query.filter(Friendship.sender_id == requester_id and Friendship.reciever_id == reciever_id).first().to_dict()
            return make_response(created_request, 200)
        except:
            return make_response({"message": "Either the sender or reciever of the friend request does not exist"}, 404)
        
    def patch(self):
        response = request.get_json()
        friend_request_id = int(response["friend_request_id"])
        friend_request_response = response["friend_request_response"]

        try:
            f = Friendship.query.filter(Friendship.id == friend_request_id).first()
            friend_request_reciever = User.query.filter(User.id == f.reciever_id).first()
            friend_request_reciever.respond_to_friend_request(friend_request_id, friend_request_response)
            if friend_request_response == "accepted":
                updated_friend_request = Friendship.query.filter(Friendship.id == friend_request_id).first().to_dict()
                return make_response(updated_friend_request, 200)
            elif friend_request_response == "rejected":
                return make_response({"message": "Successfully rejected friend request!"}, 200)
        except:
            return make_response({"message": f"Error, could not {friend_request_response} friend request"}, 404)
        
    
api.add_resource(Users, "/users")
api.add_resource(Friendships, "/friendships")
api.add_resource(SpecificUsers, "/users/<int:id>")
api.add_resource(FriendRequest, "/friendships/send_request")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
