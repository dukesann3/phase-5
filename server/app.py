#!/usr/bin/env python3

from flask import jsonify, request, make_response, session
from flask_restful import Resource
from sqlalchemy import and_, or_, not_
from models import User, Friendship, FriendRequestNotification, Post, Comment, PostLike, CommentLike, PostLikeNotification, CommentLikeNotification, CommentNotification
from configs import api, app, db, cache
import ipdb
import urllib.request
import os
import shutil
from errors import raise_error, NetworkError, ValidationError, AuthenticationError, AuthorizationError, DatabaseError, error_to_dict, network_error
from image import image_to_base64_uri

#============= Error Handling ==============================================#

class NoSearchResultsError(Exception):
    def __init__(self, message="No results found"):
        self.message = message
        super().__init__(self.message)

class NoSearchQueryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class NetworkError(Exception):
    def __init__(self, message="Network Error"):
        self.message = message
        super().__init__(self.message)

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
    
    def post(self):
        print('post-test-post')
        response = request.get_json()
    
        try:
            user_id = session["user_id"]
            new_post = Post(
                caption=response["caption"],
                user_id=user_id
            )
            db.session.add(new_post)
            db.session.commit()

            return make_response(new_post.to_dict(), 200)
        except:
            return make_response({"message": "Error, new post could not be created"}, 404)
    
class CommentTest(Resource):
    def get(self):
        all_comments = [comment.to_dict() for comment in Comment.query.all()]
        return make_response(all_comments, 200)
    
class PostLikeNotificationsTest(Resource):
    def get(self):
        all_post_like_note = [pln.to_dict() for pln in PostLikeNotification.query.all()]
        return make_response(all_post_like_note, 200)
    
class CommentNotificationsTest(Resource):
    def get(self):
        all_cn = [cn.to_dict() for cn in CommentNotification.query.all()]
        return make_response(all_cn, 200)
    
class CommentLikeNotificationTest(Resource):
    def get(self):
        all_cln = [cln.to_dict() for cln in CommentLikeNotification.query.all()]
        return make_response(all_cln, 200)
    
class UserDelete(Resource):
    def delete(self, user_id):
        print("user-delete")
        try:
            user_to_delete = User.query.filter(User.id == user_id).first()
            db.session.delete(user_to_delete)
            db.session.commit()
            session.pop('user_id', default=None)
            session.pop('n_of_users', default=None)
            shutil.rmtree(f'../../client/phase-5-project/public/images/{user_id}_folder', ignore_errors=True)
            return make_response({"message": "Successfully deleted user"}, 204)
        except:
            return make_response({"message": "Could not delete user"}, 404)
        
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

#============ For Testing Purposes Only!!! ==================================#

@app.before_request
def check_user_session():
    endpoints_without_session_check = ["login", "logout", "checksession", "onuserlistrefresh", 
                                       "createanaccount", "testcreateanaccount"]
    if request.endpoint not in endpoints_without_session_check and "user_id" not in session:
        #may need a try except block. Need testing
        raise_error("AUTHZ-001")


class Login(Resource):
    def post(self):
        print("login-post")
        try:
            response = request.get_json()
            potential_user = User.query.filter(User.username == response["username"]).first()

            try:
                potential_user.authenticate(response["password"])
            except:
                raise raise_error("AUTH-001")
            
            if potential_user.authenticate(response["password"]):
                session["user_id"] = potential_user.id
                session["n_of_users"] = 0
                return make_response(potential_user.to_dict(), 200)
        except AuthenticationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
    
class Logout(Resource):
    def delete(self):
        print('logout-delete')
        session.pop('user_id', default=None)
        session.pop('n_of_users', default=None)
        cache.clear()
        return make_response({"message": "Logout successful"}, 204)
    
class CheckSession(Resource):
    def get(self):
        print('checksession-get')
        try:
            user = User.query.filter(User.id == session["user_id"]).first()
            if user:
                return make_response(user.to_dict(), 200)
            else:
                raise_error("AUTHZ-001")
        except AuthorizationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

class Users(Resource):
    def patch(self, user_id):
        print("user-patch")
        response = request.get_json()
        try:
            user_to_patch = User.query.filter(User.id == user_id).first()
            all_attr = user_to_patch.__dict__
            for attr in all_attr:
                if response.get(attr):
                    setattr(user_to_patch, attr, response[attr])

            if response.get("image_uri"):
                image_uri = response["image_uri"]
                resp = urllib.request.urlopen(image_uri)
                profile_picture_path = f'../client/phase-5-project/public/images/{user_to_patch.id}_folder/{user_to_patch.id}_profile_picture_folder/{user_to_patch.id}_profile.jpg'
                src = f'/images/{user_to_patch.id}_folder/{user_to_patch.id}_profile_picture_folder/{user_to_patch.id}_profile.jpg'
                with open(profile_picture_path, 'wb') as f:
                    f.write(resp.file.read())
                setattr(user_to_patch, "image_src", src)

                if image_to_base64_uri(profile_picture_path) not in response["image_uri"]:
                    raise_error("DB-001")

            db.session.commit()
    
            return make_response(user_to_patch.to_dict(), 200)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

    def delete(self, user_id):
        print("user-delete")
        try:
            user_to_delete = User.query.filter(User.id == user_id).first()
            db.session.delete(user_to_delete)
            db.session.commit()
            session.pop('user_id', default=None)
            session.pop('n_of_users', default=None)
            profile_path_to_delete = f'../client/phase-5-project/public/images/{user_id}_folder'
            shutil.rmtree(profile_path_to_delete, ignore_errors=True)
            
            if os.path.exists(profile_path_to_delete):
                raise_error("DB-002")

            return make_response({"message": "Successfully deleted user"}, 204)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
        
class UserPassword(Resource):
    def patch(self, user_id):
        try:
            response = request.get_json()
            password = response["password"]

            if len(password) < 5:
                raise_error("VAL-007")

            user = User.query.filter(User.id == user_id).first()
            user.password_hash = password
            db.session.commit()
            return make_response({"message": "Password has been updated successfully"}, 200)
        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

class UserSearch(Resource):
    def post(self):
        try:
            response = request.get_json()
            search_query = response["search_query"]
            if not search_query:
                raise_error("VAL-001")
            
            search_query_w_wildcard = search_query + "%"
            previous_search_results = cache.get('search_results')
            previous_search_query = cache.get('search_query')

            logged_in_user = User.query.filter(User.id == session["user_id"]).first()
            logged_in_user_dict = logged_in_user.to_dict()
            logged_in_user_friends = [friend.to_dict() for friend in logged_in_user.friends]

            logged_in_user_pending_friends = [friend.to_dict() for friend in logged_in_user.pending_friends]

            #first time searching here and when user deletes a letter from the search query
            if (not previous_search_results and not previous_search_query and search_query) or \
                (len(previous_search_query) > len(search_query)):

                filtered_users = [user.to_dict() for user in User.query.filter(User.username.like(search_query_w_wildcard)).all()
                                  if user.to_dict() not in logged_in_user_friends and user.to_dict() not in logged_in_user_pending_friends]
                search_results = []

                for friend in logged_in_user_friends:
                    if friend["username"] == search_query:
                        continue

                    elif search_query.lower() in friend["username"].lower():
                        friend_status = {"isFriend": True, "isPending": False}
                        search_results.append({**friend, **friend_status})

                for friend in logged_in_user_pending_friends:
                    if friend["username"] == search_query:
                        continue

                    elif search_query.lower() in friend["username"].lower():
                        friend_status = {"isFriend": False, "isPending": True}
                        search_results.append({**friend, **friend_status})

                for user in filtered_users:
                    if user == logged_in_user_dict or user["username"] == search_query:
                        continue
                    else:
                        friend_status = {"isFriend": False, "isPending": False}
                        search_results.append({**user, **friend_status})

                combined = filtered_users + logged_in_user_friends
                combined_filtered = [user for user in combined if user != logged_in_user_dict]

                for user in combined_filtered:
                    if user["username"] == search_query:
                        if user in logged_in_user_friends:
                            friend_status = {"isFriend": True, "isPending": False}
                        elif user in logged_in_user_pending_friends:
                            friend_status = {"isFriend": False, "isPending": True}
                        else:
                            friend_status = {"isFriend": False, "isPending": False}

                        search_results.insert(0, {**user, **friend_status})
                
                cache.set('search_results', search_results, timeout=60)
                cache.set('search_query', search_query, timeout=60)

                if len(search_results) == 0:
                    raise_error("VAL-002")

                return make_response(search_results, 200)

            elif len(previous_search_query) < len(search_query) and previous_search_results:
                search_results = [user for user in previous_search_results if search_query in user["username"]]
                cache.set('search_results', search_results, timeout=60)
                cache.set('search_query', search_query, timeout=60)
                if len(search_results) == 0:
                    raise_error("VAL-002")

                return make_response(search_results, 200)
            else:
                raise_error("VAL-002")
        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

class Friends(Resource):
    def get(self):
        user_id = session['user_id']
        try:
            user = User.query.filter(User.id == user_id).first()
            friends = []

            for friend in user.all_friends:
                friend_to_add = friend["value"].to_dict()
                friend_to_add["status"] = friend["status"]
                friends.append(friend_to_add)

            return make_response(friends, 200)
        except:
            return make_response(network_error, 404)
    
class FriendsEdit(Resource):
    def delete(self, f_id):
        print("start")
        user_id = session["user_id"]
        friend_id = f_id
        try:
            friendship_to_delete = Friendship.query.filter(or_(
                and_(Friendship.reciever_id == user_id, Friendship.sender_id == friend_id),
                and_(Friendship.sender_id == user_id, Friendship.reciever_id == friend_id)
            )).first()
            db.session.delete(friendship_to_delete)
            db.session.commit()
            return make_response({"message": "Friend deleted successfully"},200)
        except:
            return make_response(network_error, 404)


class FriendRequest(Resource):
    def post(self):
        print('friendrequest-post')
        response = request.get_json()
        requester_id = int(response["sender_id"])
        reciever_id = int(response["reciever_id"])

        try:
            requester = User.query.filter(User.id == requester_id).first()

            try:
                requester.send_friend_request(reciever_id)
            except:
                raise_error("VAL-003")

            created_request = Friendship.query.filter(Friendship.sender_id == requester_id, 
                                                      Friendship.reciever_id == reciever_id).first().to_dict()
            return make_response(created_request, 200)
        except:
            return make_response({"error": "Either the sender or reciever of the friend request does not exist"}, 404)
        
    def patch(self):
        print('friendrequest-patch')
        try:
            response = request.get_json()
            friend_request_id = int(response["friend_request_id"])
            friend_request_response = response["friend_request_response"]
            if friend_request_response not in ["accepted", "rejected"]:
                raise_error("VAL-004")

            f = Friendship.query.filter(Friendship.id == friend_request_id).first()
            friend_request_reciever = User.query.filter(User.id == f.reciever_id).first()
            try:
                friend_request_reciever.respond_to_friend_request(friend_request_id, friend_request_response)
            except:
                raise_error("VAL-005")

            if friend_request_response == "accepted":
                updated_friend_request = Friendship.query.filter(Friendship.id == friend_request_id).first().to_dict()
                return make_response(updated_friend_request, 200)
            elif friend_request_response == "rejected":
                return make_response({"message": "Successfully rejected friend request!"}, 200)  
            else:
                raise_error("NET-001")   

        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
        
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
            return make_response(network_error, 404)
        
    def post(self):
        print('post-post')
        try:
            response = request.get_json()
            user_id = session["user_id"]
            image_uri = response["image_uri"]
            try:
                new_post = Post(
                    location=response["location"],
                    caption=response["caption"],
                    user_id=user_id
                )
                db.session.add(new_post)
                db.session.commit()
            except:
                raise_error("VAL-006")

            if image_uri:
                resp = urllib.request.urlopen(image_uri)
                new_post_path = f'../client/phase-5-project/public/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{new_post.id}.jpg'
                with open(new_post_path, 'wb') as f:
                    f.write(resp.file.read())
                if os.path.exists(new_post_path):
                    new_post.image_src = f'/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{new_post.id}.jpg'
                    db.session.commit()

                if not os.path.exists(new_post_path):
                    raise_error("DB-003")

            return make_response(new_post.to_dict(), 200)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except ValidationError as e:
            return make_response(error_to_dict(e), 401)
        except:
            return make_response(network_error, 404)
        
class PostEdit(Resource):
    def delete(self, p_id):
        try:
            post_to_delete = Post.query.filter(Post.id == p_id).first()
            user_id = post_to_delete.user_id
            post_id = post_to_delete.id

            db.session.delete(post_to_delete)
            db.session.commit()

            profile_path_to_delete = f'../client/phase-5-project/public/images/{user_id}_folder/{user_id}_posts_folder/{user_id}_{post_id}.jpg'
            shutil.rmtree(profile_path_to_delete, ignore_errors=True)

            if os.path.exists(profile_path_to_delete):
                raise_error("DB-004")

            return make_response({"message": "Post has been succesfully deleted"}, 204)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
        
    def patch(self, p_id):
        response = request.get_json()
        try:
            post_to_patch = Post.query.filter(Post.id == p_id).first()
            poster_id = post_to_patch.user_id
            post_id = post_to_patch.id
            all_attr = post_to_patch.__dict__

            for attr in all_attr:
                if response.get(attr):
                    setattr(post_to_patch, attr, response[attr])
            if response.get("image_uri"):
                image_uri = response["image_uri"]
                resp = urllib.request.urlopen(image_uri)
                post_path = f'../client/phase-5-project/public/images/{poster_id}_folder/{poster_id}_posts_folder/{poster_id}_{post_id}.jpg'
                src = f'/images/{poster_id}_folder/{poster_id}_posts_folder/{poster_id}_{post_id}.jpg'
                with open(post_path, 'wb') as f:
                    f.write(resp.file.read())
                setattr(post_to_patch, "_image_src", src)

                if image_to_base64_uri(post_path) not in response["image_uri"]:
                    raise_error("DB-004")

            db.session.commit()
            return make_response(post_to_patch.to_dict(), 200)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

        
class CreateAnAccount(Resource):
    def post(self):
        print('createanaccount-post')
        try:
            response = request.get_json()
            first_name = response["first_name"]
            last_name = response["last_name"]
            username = response["username"]
            image_uri = response["image_uri"]
            password = response["password"]

            if len(password) < 5:
                raise_error("VAL-007")

            try:
                new_user = User(first_name=first_name,
                                last_name=last_name,
                                username=username)
                new_user.password_hash = password
                db.session.add(new_user)
                db.session.commit()
            except:
                raise_error("VAL-008")

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

                if not os.path.exists(profile_picture_path):
                    raise_error("DB-005")
        
            return make_response(new_user.to_dict(), 200)
        except DatabaseError as e:
            return make_response(error_to_dict(e), 400)
        except ValidationError as e:
            return make_response(error_to_dict(e), 401)
        except:
            return make_response({"error": "Error, new user could not be made"}, 404)

#repurpose later
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

            try:
                new_comment = Comment(post_id=post_id, user_id=user_id, text=text)
                db.session.add(new_comment)
                db.session.commit()
            except: 
                raise_error("VAL-009")

            reciever = Post.query.filter(Post.id == post_id).first().user
            sender_username = User.query.filter(User.id == user_id).first().username
            reciever_id = reciever.id
            reciever_username = reciever.username

            if user_id != reciever_id:
                cn = CommentNotification(
                    sender_id=user_id,
                    reciever_id=reciever_id,
                    comment_id=new_comment.id,
                    text=f"{sender_username} commented on {reciever_username}'s post"
                )
                db.session.add(cn)
                db.session.commit()

            return make_response(new_comment.to_dict(), 200)
        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
    
class CommentEdit(Resource):
    def patch(self, c_id):
        print("comment-patch")
        response = request.get_json()

        try:
            comment_to_patch = Comment.query.filter(Comment.id == c_id).first()
            all_attr = comment_to_patch.__dict__
            for attr in all_attr:
                if attr == "text" and len(response[attr]) == 0:
                    raise_error("VAL-010")

                if response.get(attr):
                    setattr(comment_to_patch, attr, response[attr])

            db.session.commit()
            return make_response(comment_to_patch.to_dict(), 200)
        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
        

    def delete(self, c_id):
        try:
            comment_to_delete = Comment.query.filter(Comment.id == c_id).first()
            db.session.delete(comment_to_delete)
            db.session.commit()
            return make_response({"message": "Comment deleted successfully"}, 204)
        except:
            return make_response(network_error, 404)
        
class PostLikes(Resource):
    def post(self):
        response = request.get_json()
        try:
            isLiked = response["isLiked"]
            user_id = session["user_id"]
            post_id = response["post_id"]

            try:
                post_like = PostLike(
                    isLiked=isLiked,
                    user_id=user_id,
                    post_id=post_id
                )

                db.session.add(post_like)
                db.session.commit()
            except:
                raise_error("VAL-011")

            sender_username = User.query.filter(User.id == user_id).first().username
            reciever_id = Post.query.filter(Post.id == post_id).first().user_id

            if user_id != reciever_id:
                post_like_notification = PostLikeNotification(
                    sender_id=user_id,
                    reciever_id=reciever_id,
                    post_id=post_id,
                    text=f"{sender_username} liked your post"
                )
                db.session.add(post_like_notification)
                db.session.commit()
            return make_response(post_like.to_dict(), 200)
        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)

class PostDislike(Resource):
    def delete(self, post_like_id):
        try:
            post_dislike= PostLike.query.filter(PostLike.id == post_like_id).first()
            db.session.delete(post_dislike)
            db.session.commit()
            return make_response({"message": "Post dislike successful"}, 204)
        except:
            return make_response(network_error, 404)     

class CommentLikes(Resource):
    def post(self):
        response = request.get_json()
        try:
            liker_id = session["user_id"]
            isLiked = response["isLiked"]
            comment_id = response["comment_id"]

            try:
                comment_like = CommentLike(
                    isLiked=isLiked,
                    user_id=liker_id,
                    comment_id=comment_id
                )
                db.session.add(comment_like)
                db.session.commit()
            except:
                raise_error("VAL-012")

            comment = Comment.query.filter(Comment.id == comment_id).first()
            commenter_id = comment.user_id
            commenter_username = comment.user.username

            post = Post.query.filter(Post.id == comment.post_id).first()
            poster_id = post.user_id

            liker_username = User.query.filter(User.id == liker_id).first().username

            if liker_id == poster_id:
                cln = CommentLikeNotification(
                    sender_id=liker_id,
                    reciever_id=commenter_id,
                    comment_id=comment_id,
                    text=f"{liker_username} liked {commenter_username}'s comment"
                )
                db.session.add(cln)
                db.session.commit()
                return make_response(cln.to_dict(), 200)

            elif liker_id == commenter_id:
                cln = CommentLikeNotification(
                    sender_id=liker_id,
                    reciever_id=poster_id,
                    comment_id=comment_id,
                    text=f"{liker_username} liked {commenter_username}'s comment"
                )
                db.session.add(cln)
                db.session.commit()
                return make_response(cln.to_dict(), 200)
            
            else:
                cln1 = CommentLikeNotification(
                    sender_id=liker_id,
                    reciever_id=poster_id,
                    comment_id=comment_id,
                    text=f"{liker_username} liked {commenter_username}'s comment"
                )

                cln2 = CommentLikeNotification(
                    sender_id=liker_id,
                    reciever_id=commenter_id,
                    comment_id=comment_id,
                    text=f"{liker_username} liked {commenter_username}'s comment"
                )

                db.session.add_all([cln1, cln2])
                db.session.commit()

                all_cln = [cln1, cln2]
                all_cln_dict = [cln.to_dict() for cln in all_cln]
                return make_response(all_cln_dict, 200)

        except ValidationError as e:
            return make_response(error_to_dict(e), 400)
        except:
            return make_response(network_error, 404)
        
class CommentDislike(Resource):
    def delete(self, comment_like_id):
        try:
            comment_dislike = CommentLike.query.filter(CommentLike.id == comment_like_id).first()
            db.session.delete(comment_dislike)
            db.session.commit()
            return make_response({"message": "Comment dislike successful"}, 204)
        except:
            return make_response(network_error, 404)
        
class CommentNotifications(Resource):
    def delete(self, cn_id):
        try:
            cn = CommentNotification.query.filter_by(id=cn_id).first()
            db.session.delete(cn)
            db.session.commit()
            return make_response({"message": "Comment notification deleted successfully"}, 204)
        except:
            return make_response(network_error, 404)

class CommentLikeNotifications(Resource):
    def delete(self, cln_id):
        try:
            cln = CommentLikeNotification.query.filter_by(id=cln_id).first()
            db.session.delete(cln)
            db.session.commit()
            return make_response({"message": "Comment like notification deleted successfully"}, 204)
        except:
            return make_response(network_error, 404)

class PostLikeNotifications(Resource):
    def delete(self, pln_id):
        try:
            pln = PostLikeNotification.query.filter_by(id=pln_id).first()
            db.session.delete(pln)
            db.session.commit()
            return make_response({"message": "Post like notification deleted successfully"}, 204)
        except:
            return make_response(network_error, 404)

api.add_resource(Users, "/users/<int:user_id>")
api.add_resource(UserTest, '/all_users')
api.add_resource(CreateAnAccount, '/create_an_account')
api.add_resource(onUserListRefresh, "/onrefresh")
api.add_resource(FriendRequest, "/friendships/send_request")
api.add_resource(UserPassword, "/users/password/<int:user_id>")
api.add_resource(UserSearch, "/user/search")

api.add_resource(Friends, "/user/friends")
api.add_resource(FriendsEdit, "/user/friends/<int:f_id>")

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

api.add_resource(CheckSession, "/checksession")

api.add_resource(Posts, "/posts", endpoint="check_session")
api.add_resource(PostEdit, "/post/<int:p_id>")
api.add_resource(PostLikes, "/post/like")
api.add_resource(PostDislike, "/post/like/<int:post_like_id>")

api.add_resource(Comments, '/comment')
api.add_resource(CommentNotifications, '/comment/notification/<int:cn_id>')
api.add_resource(CommentEdit, '/comment/<int:c_id>')
api.add_resource(CommentLikes, '/comment/like')
api.add_resource(CommentDislike, '/comment/like/<int:comment_like_id>')
api.add_resource(CommentLikeNotifications, '/comment/like/notification/<int:cln_id>')

#for testing purposes only-----------------------------------------------------
api.add_resource(TestCreateAnAccount, "/test_create_an_account")
api.add_resource(UserTestSpecifics, "/user_test/<int:user_id>")
api.add_resource(FriendshipTest, "/friendships")
api.add_resource(FriendshipTestSpecifics, "/friendship_test/<int:f_id>")
api.add_resource(FRNotificationTestSpecifics, "/friend_request_notification_test/<int:n_id>")
api.add_resource(PostTest, '/post_test')
api.add_resource(CommentTest, '/comment_test')
api.add_resource(PostLikeNotificationsTest, '/pln_test')
api.add_resource(CommentNotificationsTest, '/cn_test')
api.add_resource(CommentLikeNotificationTest, '/cln_test')
api.add_resource(UserDelete, '/user_test/delete/<int:user_id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
