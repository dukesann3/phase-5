#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Friendship, Notification

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)
api = Api(app)

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)
    
class Friendships(Resource):
    def get(self):
        friendships = [friendship.to_dict() for friendship in Friendship.query.all()]
        return make_response(friendships, 200)
    
class FriendshipRequest(Resource):
    def post(self):
        response = request.get_json()
        try:
            sender = User.query.filter(User.id == response["sender_id"]).first()
            sender.send_friend_request(response["reciever_id"])
            return make_response({"message": "Friend request sent!"}, 200)
        except:
            return make_response({"message": "Friend request could not be sent"}, 404)

api.add_resource(Users, "/users")
api.add_resource(Friendships, "/friendships")
api.add_resource(FriendshipRequest, "/friendships/request")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
