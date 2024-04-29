#!/usr/bin/env python3

from flask import jsonify, request, make_response, session
from flask_restful import Resource
from models import User, Friendship, Notification, Post, Comment, PostLike, CommentLike
from configs import api, app, db
import ipdb
import urllib.request
import os

# @app.before_request
# def check_if_logged_in():
#     if not session['user_id'] and request.endpoint != 'check_session' :
#         return {'error': 'Unauthorized'}, 401


#============ For Testing Purposes Only!!! ==================================#
class Friendships(Resource):
    def get(self):
        friendships = [friendship.to_dict() for friendship in Friendship.query.all()]
        return make_response(friendships, 200)
    
class UserTest(Resource):
    def get(self):
        all_users = [user.to_dict() for user in User.query.all()]
        return make_response(all_users, 200)
#============ For Testing Purposes Only!!! ==================================#

class Login(Resource):
    def post(self):
        print("login-get")
        response = request.get_json()
        potential_user = User.query.filter(User.username == response["username"]).first()
        print(potential_user)
        
        try:
            if potential_user.authenticate(response["password"]):

                session["user_id"] = potential_user.id
                session["n_of_users"] = 0

                return make_response(potential_user.to_dict(), 200)
        except:
            return make_response({"message": "Error, could not find username or password in database"}, 404)
    
class Logout(Resource):
    def delete(self):
        print('logout-delete')
        session.pop('user_id', default=None)
        session.pop('n_of_users', default=None)

        return make_response({"message": "Logout successful"}, 204)
    
class CheckSession(Resource):
    def get(self):
        print('checksession-get')
        try:
            user = User.query.filter(User.id == session["user_id"]).first()
            if user:
                return make_response(user.to_dict(), 200)
            else:
                return make_response({"message": "Error, could not find user data in session"}, 404)
        except:
            return make_response({"message": "Network Error"}, 500)

class Users(Resource):
    def get(self, user_id):
        print('users-get')
        n_of_users_per_click = 3
        loggedInUser = User.query.filter(User.id == user_id).first()

        try:
            if len(User.query.all()) > session["n_of_users"]:
                session["n_of_users"] = session["n_of_users"] + n_of_users_per_click
            elif len(User.query.all()) <= session["n_of_users"]:
                raise ValueError("Exceeded the amount of user requests")
            
            n_of_users = session["n_of_users"]
            users = []

            for user in User.query.all():
                if user in loggedInUser.friends or user == loggedInUser:
                    continue
                users.append(user)
            
            print(users)
            users_dict = [user.to_dict() for user in users]
            users_dict_return = users_dict[:n_of_users]

            return make_response(users_dict_return, 200)

        except ValueError as error:
            return make_response({"message": f"{error}"}, 401)
        except:
            return make_response({"message": "Error, could not fetch users"}, 402)
    

class SpecificUsers(Resource):
    def get(self, id):
        print('specificusers-get')
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
        print('friendrequest-post')
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
        print('friendrequest-patch')
        response = request.get_json()
        friend_request_id = int(response["friend_request_id"])
        friend_request_response = response["friend_request_response"]
        print("where?")
        try:
            print("hh")
            f = Friendship.query.filter(Friendship.id == friend_request_id).first()
            print("h2")
            friend_request_reciever = User.query.filter(User.id == f.reciever_id).first()
            print("h3")
            print(friend_request_reciever.username)
            print(friend_request_id)
            print(friend_request_response)
            friend_request_reciever.respond_to_friend_request(friend_request_id, friend_request_response)
            print("am I here?")
            if friend_request_response == "accepted":
                updated_friend_request = Friendship.query.filter(Friendship.id == friend_request_id).first().to_dict()
                return make_response(updated_friend_request, 200)
            elif friend_request_response == "rejected":
                return make_response({"message": "Successfully rejected friend request!"}, 200)     
            else:
                raise ValueError("Friend request response must be either accepted or rejected", 400)
        except ValueError as err:
            return make_response({"message": err}, )
        except:
            return make_response({"message": f"Error, could not {friend_request_response} friend request"}, 404)
        

        
class Posts(Resource):
    def get(self):
        print('post-get')
        try:
            user_id = session["user_id"]
            user = User.query.filter(User.id == user_id).first()
            friends = user.friends
            post_list = []

            for friend in friends:
                for post in friend.posts:
                    post_list.append(post)
            
            sorted_post_list = sorted(post_list, key=lambda post: post["updated_at"])
            sorted_post_list_to_dict = [post.to_dict() for post in sorted_post_list]

            return make_response(sorted_post_list_to_dict, 200)
        
        except:
            return make_response({"message": "Error, could not retrieve all posts"}, 404)
        

    def post(self):
        print('post-post')
        response = request.get_json()
    
        try:

            user_id = session["user_id"]
            image_uri = response["image_uri"]

            new_post = Post(
                location=response["location"],
                caption=response["caption"],
                user_id=user_id
            )

            db.session.add(new_post)
            db.session.commit()

            if image_uri:
                resp = urllib.request.urlopen(image_uri)
                new_post_path = f'../client/phase-5-project/public/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{new_post.id}.jpg'
                with open(new_post_path, 'wb') as f:
                    f.write(resp.file.read())
                if os.path.exists(new_post_path):
                    print("path?")
                    new_post.image_src = f'/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{new_post.id}.jpg'
                    db.session.commit()

            return make_response(new_post.to_dict(), 200)
        except:
            return make_response({"message": "Error, new post could not be created"}, 404)
        
class CreateAnAccount(Resource):
    def post(self):
        print('createanaccount-post')
        response = request.get_json()
        first_name = response["first_name"]
        last_name = response["last_name"]
        username = response["username"]
        image_uri = response["image_uri"]

        try:
            print("here?")
            new_user = User(first_name=first_name,
                            last_name=last_name,
                            username=username)
            new_user.password_hash = response["password"]
            print("nn")
            db.session.add(new_user)
            print("ff")
            print(first_name, last_name, username, image_uri)
            db.session.commit()
            print("yeah?")
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder")
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder/{new_user.id}_profile_picture_folder")
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder/{new_user.id}_posts_folder")
            print("huh?")
            if image_uri:
                resp = urllib.request.urlopen(image_uri)
                profile_picture_path = f'../client/phase-5-project/public/images/{new_user.id}_folder/{new_user.id}_profile_picture_folder/{new_user.id}_profile.jpg'
                with open(profile_picture_path, 'wb') as f:
                    f.write(resp.file.read())
                if os.path.exists(profile_picture_path):
                    new_user.image_src = f'/images/{new_user.id}_folder/{new_user.id}_profile_picture_folder/{new_user.id}_profile.jpg'
                    db.session.commit()

            return make_response(new_user.to_dict(), 200)
        except:
            return make_response({"message": "Error, new user could not be made"}, 404)
        
class onUserListRefresh(Resource):
    def delete(self):
        session['n_of_users'] = 0

        return make_response({"message": "Session cookie has been successfully changed"}, 200)

    
api.add_resource(Users, "/users/<int:user_id>")
api.add_resource(Friendships, "/friendships")
api.add_resource(SpecificUsers, "/users/<int:id>")
api.add_resource(FriendRequest, "/friendships/send_request")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
#should run this whenever the user first lands, so use useEffect
api.add_resource(CheckSession, "/checksession")
api.add_resource(Posts, "/posts", endpoint="check_session")
api.add_resource(onUserListRefresh, "/onrefresh")
api.add_resource(UserTest, '/all_users')
api.add_resource(CreateAnAccount, '/create_an_account')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
