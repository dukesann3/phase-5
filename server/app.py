#!/usr/bin/env python3

from flask import jsonify, request, make_response, session
from flask_restful import Resource
from models import User, Friendship, FriendRequestNotification, Post, Comment, PostLike, CommentLike
from configs import api, app, db
import ipdb
import urllib.request
import os

# @app.before_request
# def check_if_logged_in():
#     if not session['user_id'] and request.endpoint != 'check_session' :
#         return {'error': 'Unauthorized'}, 401


#============ For Testing Purposes Only!!! ==================================#

class FriendshipTest(Resource):
    def get(self):
        friendships = [friendship.to_dict() for friendship in Friendship.query.all()]
        return make_response(friendships, 200)
    
class FriendshipTestSpecifics(Resource):
    def get(self, f_id):
        try:
            friendship = Friendship.query.filter(Friendship.id == f_id).first().to_dict()
            return make_response(friendship, 200)
        except:
            return make_response({"message": "Error, friend request could not be found"}, 404)
        
class FRNotificationTestSpecifics(Resource):
    def get(self, n_id):
        try:
            notification = FriendRequestNotification.query.filter(FriendRequestNotification.id == n_id).first().to_dict()
            return make_response(notification, 200)
        except:
            return make_response({"message": "Error, notification could not be found"}, 404)
    
class UserTest(Resource):
    def get(self):
        all_users = [user.to_dict() for user in User.query.all()]
        return make_response(all_users, 200)
    
class UserTestSpecifics(Resource):
    def get(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        return make_response(user.to_dict(), 200)
    
class PostTest(Resource):
    def get(self):
        all_posts = [post.to_dict() for post in Post.query.all()]
        return make_response(all_posts, 200)

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
        try:
            f = Friendship.query.filter(Friendship.id == friend_request_id).first()
            friend_request_reciever = User.query.filter(User.id == f.reciever_id).first()
            friend_request_reciever.respond_to_friend_request(friend_request_id, friend_request_response)
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
            user_and_friends = user.friends + [user]
            post_list = []

            for people in user_and_friends:
                for post in people.posts:
                    post_list.append(post)
            
            sorted_post_list = sorted(post_list, key=lambda post: post.updated_at)
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
                    new_post.image_src = f'/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{new_post.id}.jpg'
                    db.session.commit()

            return make_response(new_post.to_dict(), 200)
        except:
            return make_response({"message": "Error, new post could not be created"}, 404)
        
class PostEdit(Resource):
    def delete(self, p_id):
        try:
            post_to_delete = Post.query.filter(Post.id == p_id).first()
            print(post_to_delete.user_id, session["user_id"])
            if post_to_delete.user_id != session["user_id"]:
                raise ValueError("user does not have the credentials to edit this post")
            
            db.session.delete(post_to_delete)
            db.session.commit()
            return make_response({"message": "Post has been succesfully deleted"}, 204)
        
        except ValueError as err:
            return make_response({"message": err}, 402)
        except:
            return make_response({"message": "Error, post cannot be found"}, 404)
        
    def patch(self, p_id):
        response = request.get_json()

        try:
            post_to_patch = Post.query.filter(Post.id == p_id).first()
            all_attr = post_to_patch.__dict__
            for attr in all_attr:
                if response.get(attr):
                    setattr(post_to_patch, attr, response[attr])

            db.session.commit()
            return make_response(post_to_patch.to_dict(), 200)
        except:
            return make_response({"message": "Error, could not patch post"}, 404)

        
class CreateAnAccount(Resource):
    def post(self):
        print('createanaccount-post')
        response = request.get_json()
        
        first_name = response["first_name"]
        last_name = response["last_name"]
        username = response["username"]
        image_uri = response["image_uri"]

        try:
            new_user = User(first_name=first_name,
                            last_name=last_name,
                            username=username)
            new_user.password_hash = response["password"]
            db.session.add(new_user)
            db.session.commit()
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder")
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder/{new_user.id}_profile_picture_folder")
            os.mkdir(f"../client/phase-5-project/public/images/{new_user.id}_folder/{new_user.id}_posts_folder")
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
        
class TestCreateAnAccount(Resource):
    def post(self):
        response = request.get_json()
        first_name = response["first_name"]
        last_name = response["last_name"]
        username = response["username"]
        # image_uri = response["image_uri"]

        try:
            new_user = User(first_name=first_name,
                            last_name=last_name,
                            username=username)
            new_user.password_hash = response["password"]
            db.session.add(new_user)
            db.session.commit()
            return make_response(new_user.to_dict(), 200)
        except:
            return make_response({"message": "Error, new user could not be made"}, 403)
        
class onUserListRefresh(Resource):
    def delete(self):
        session['n_of_users'] = 0

        return make_response({"message": "Session cookie has been successfully changed"}, 200)
    
class Comments(Resource):
    def post(self):
        print("comment-post")
        response = request.get_json()

        try:
            post_id = response["post_id"]
            text = response["text"]
            user_id = session["user_id"]

            new_comment = Comment(post_id=post_id, user_id=user_id, text=text)
            db.session.add(new_comment)
            db.session.commit()
            return make_response(new_comment.to_dict(), 200)
        except:
            return make_response({"message": "Error, could not create new comment"}, 404)
    
class CommentEdit(Resource):
    def patch(self, c_id):
        print("comment-patch")
        response = request.get_json()

        try:
            comment_to_patch = Comment.query.filter(Comment.id == c_id).first()
            all_attr = comment_to_patch.__dict__
            for attr in all_attr:
                if response.get(attr):
                    setattr(comment_to_patch, attr, response[attr])

            db.session.commit()
            return make_response(comment_to_patch.to_dict(), 200)
        except:
            return make_response({"message": "Error, could not patch post"}, 404)
        

    def delete(self, c_id):
        try:
            comment_to_delete = Comment.query.filter(Comment.id == c_id).first()
            db.session.delete(comment_to_delete)
            db.session.commit()
            return make_response({"message": "Comment deleted successfully"}, 204)
        except:
            return make_response({"message": "Error, comment could not be deleted"}, 404)
        
class PostLikes(Resource):
    def post(self):
        response = request.get_json()
        try:
            post_like = PostLike(
                isLiked=response["isLiked"],
                user_id=session["user_id"],
                post_id=response["post_id"]
            )
            db.session.add(post_like)
            db.session.commit()

            return make_response(post_like.to_dict(), 200)
        except:
            return make_response({"message": "Error, post could not be liked"}, 404)

class PostLikeDelete(Resource):
    def delete(self, post_like_id):
        try:
            post_like_to_delete = PostLike.query.filter(PostLike.id == post_like_id).first()
            db.session.delete(post_like_to_delete)
            db.session.commit()
            return make_response({"message": "Post like deleted successfully"}, 204)
        except:
            return make_response({"message": "Error, post like could not be deleted"}, 404)     

class CommentLikes(Resource):
    def post(self):
        response = request.get_json()
        try:
            comment_like = CommentLike(
                isLiked=response["isLiked"],
                user_id=session["user_id"],
                comment_id=response["comment_id"]
            )
            db.session.add(comment_like)
            db.session.commit()

            return make_response(comment_like.to_dict(), 200)
        except:
            return make_response({"message": "Error, comment could not be liked"}, 404)
        
class CommentLikeDelete(Resource):
    def delete(self, comment_like_id):
        try:
            comment_like_to_delete = CommentLike.query.filter(CommentLike.id == comment_like_id).first()
            db.session.delete(comment_like_to_delete)
            db.session.commit()
            return make_response({"message": "Comment like deleted successfully"}, 204)
        except:
            return make_response({"message": "Error, comment like could not be deleted"}, 404) 


api.add_resource(Users, "/users/<int:user_id>")
api.add_resource(SpecificUsers, "/users/<int:id>")
api.add_resource(UserTest, '/all_users')
api.add_resource(CreateAnAccount, '/create_an_account')
api.add_resource(onUserListRefresh, "/onrefresh")
api.add_resource(FriendRequest, "/friendships/send_request")

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

api.add_resource(CheckSession, "/checksession")

api.add_resource(Posts, "/posts", endpoint="check_session")
api.add_resource(PostEdit, "/post/<int:p_id>")
api.add_resource(PostLikes, "/post/like")
api.add_resource(PostLikeDelete, "/post/like/<int:post_like_id>")

api.add_resource(Comments, '/comment')
api.add_resource(CommentEdit, '/comment/<int:c_id>')
api.add_resource(CommentLikes, '/comment/like')
api.add_resource(CommentLikeDelete, '/comment/like/<int:comment_like_id>')

#for testing purposes only-----------------------------------------------------
api.add_resource(TestCreateAnAccount, "/test_create_an_account")
api.add_resource(UserTestSpecifics, "/user_test/<int:user_id>")
api.add_resource(FriendshipTest, "/friendships")
api.add_resource(FriendshipTestSpecifics, "/friendship_test/<int:f_id>")
api.add_resource(FRNotificationTestSpecifics, "/friend_request_notification_test/<int:n_id>")
api.add_resource(PostTest, '/post_test')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
