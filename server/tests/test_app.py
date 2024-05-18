from models import User, Friendship, FriendRequestNotification, Post, PostLike, PostLikeNotification, Comment, CommentLike, CommentNotification, CommentLikeNotification
from configs import db
from app import app
from flask import Flask, url_for
import flask
import ipdb
import json
import os

def reset_all():
    User.query.delete()
    Friendship.query.delete()
    FriendRequestNotification.query.delete()
    Post.query.delete()
    PostLike.query.delete()
    PostLikeNotification.query.delete()
    Comment.query.delete()
    CommentLike.query.delete()
    CommentNotification.query.delete()
    CommentLikeNotification.query.delete()
    db.session.commit()

class TestLogAndFriendRequest:

    def test_create_account(self):
        '''Create account works'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:

            resp = client.post("/test_create_an_account",
                                          json={
                                              "first_name": "a",
                                              "last_name": "a",
                                              "username": "12345",
                                              "password": "12345"
                                          })
            
            assert(resp.status_code == 200)


    def test_login(self):
        '''User log in will have session cookies: user_id 
        and n_of_users'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:
            #create user first

            resp = client.post("/test_create_an_account",
                                          json={
                                              "first_name": "a",
                                              "last_name": "a",
                                              "username": "12345",
                                              "password": "12345"
                                          })
            
            assert(resp.status_code == 200)

            resp = client.post('/login', json={
                "username": "12345",
                "password": "12345"
            })

            assert(resp.status_code == 200)
            assert(flask.session.get('user_id') == 1)
            assert(flask.session.get('n_of_users') == 0)

    def test_logout(self):
        '''User log out will pop session cookie values '''

        with app.test_client() as client:
            
            resp = client.delete("/logout")
            assert(resp.status_code == 204)

            try:
                user_id = flask.session.get('user_id')
                n_of_users = flask.session.get('n_of_users')
                print(user_id, n_of_users)
            except:
                assert(True)

    def test_check_session(self):
        '''Check session will run and return true if
        session object for user_id is present'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:

            resp = client.post("/test_create_an_account",
                                          json={
                                              "first_name": "a",
                                              "last_name": "a",
                                              "username": "12345",
                                              "password": "12345"
                                          })
            
            assert(resp.status_code == 200)

            resp = client.post('/login', json={
                "username": "12345",
                "password": "12345"
            })

            assert(resp.status_code == 200)
            assert(flask.session.get('user_id') == 1)
            assert(flask.session.get('n_of_users') == 0)

            #run check session down here...
            
            check_session = client.get('/checksession')
            assert(check_session.status_code == 200)


    def test_send_friend_request(self):
        '''Tests if friend request will produce a friendship
        row for both request sender and reciever. And sends a notification
        only to the request reciever'''

        #check for database entries afterwards.
        with app.app_context():
            reset_all()

        with app.test_client() as client:

            resp1 = client.post("/test_create_an_account", json={"first_name": "a", "last_name": "a",
                                                                "username": "a", "password": "12345"})
            
            assert(resp1.status_code == 200)
            sender_id = resp1.json['id']

            resp2 = client.post("/test_create_an_account", json={"first_name": "b", "last_name": "b",
                                                                "username": "b", "password": "12345"})
            
            assert(resp2.status_code == 200)
            reciever_id = resp2.json['id']
            
            client.post('/friendships/send_request', json={
                "sender_id": sender_id,
                "reciever_id": reciever_id
            })

            sender = client.get(f"/user_test/{sender_id}")
            reciever = client.get(f"/user_test/{reciever_id}")

            sender_friendship = sender.json['friendships'][0]
            reciever_friendship = reciever.json['friendships'][0]

            assert(sender_friendship == reciever_friendship)
            assert(len(sender.json['friend_request_notifications']) == 0)
            assert(bool(reciever.json['friend_request_notifications'][0]) == True)


    def test_accept_friend_request(self):
        '''When friend request is accepted, the friend request
         row will change its status from pending to accepted. And 
         simultaneously delete notification from the request reciever
         regarding the friend request'''
        
        #check for database entries afterwards
        with app.app_context():
            reset_all()

        with app.test_client() as client:

            resp1 = client.post("/test_create_an_account", json={"first_name": "a", "last_name": "a",
                                                                "username": "a", "password": "12345"})
            
            assert(resp1.status_code == 200)
            sender_id = resp1.json['id']

            resp2 = client.post("/test_create_an_account", json={"first_name": "b", "last_name": "b",
                                                                "username": "b", "password": "12345"})
            
            assert(resp2.status_code == 200)
            reciever_id = resp2.json['id']
            
            client.post('/friendships/send_request', json={
                "sender_id": sender_id,
                "reciever_id": reciever_id
            })

            sender = client.get(f"/user_test/{sender_id}")
            assert(sender.status_code == 200)
            
            friendship_id = sender.json['friendships'][0]['id']
            updated_friendship = client.patch('/friendships/send_request', json={
                "friend_request_id": friendship_id,
                "friend_request_response": "accepted"
            })

            assert(updated_friendship.status_code == 200)
            assert(updated_friendship.json['_status'] == "accepted")

    def test_reject_friend_request(self):
        '''When friend request is rejected, all pending friendships will
        be deleted as well as notifications regarding it'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:

            resp1 = client.post("/test_create_an_account", json={"first_name": "a", "last_name": "a",
                                                                "username": "a", "password": "12345"})
            
            assert(resp1.status_code == 200)
            sender_id = resp1.json['id']

            resp2 = client.post("/test_create_an_account", json={"first_name": "b", "last_name": "b",
                                                                "username": "b", "password": "12345"})
            
            assert(resp2.status_code == 200)
            reciever_id = resp2.json['id']
            
            client.post('/friendships/send_request', json={
                "sender_id": sender_id,
                "reciever_id": reciever_id
            })

            sender = client.get(f"/user_test/{sender_id}")
            assert(sender.status_code == 200)
            
            friendship_id = sender.json['friendships'][0]['id']
            updated_friendship = client.patch('/friendships/send_request', json={
                "friend_request_id": friendship_id,
                "friend_request_response": "rejected"
            })

            assert(updated_friendship.status_code == 200)
            
            sender = client.get(f"/user_test/{sender_id}")
            reciever = client.get(f"/user_test/{reciever_id}")

            assert(len(sender.json['friendships']) == 0)
            assert(len(reciever.json['friendships']) == 0)
            assert(len(sender.json['friend_request_notifications']) == 0)
            assert(len(reciever.json['friend_request_notifications']) == 0)

    def test_dual_friendship_accept(self):
        '''When both users send each other friend requests
        and if one accepts, all their notifications are deleted
        and the friendship request which the user accepts will be the
        one that will remain. The other will be deleted'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:
            #creating accounts here ---------------------------------

            resp1 = client.post("/test_create_an_account", json={"first_name": "a", "last_name": "a",
                                                                "username": "a", "password": "12345"})
            
            assert(resp1.status_code == 200)
            sender_id = resp1.json['id']

            resp2 = client.post("/test_create_an_account", json={"first_name": "b", "last_name": "b",
                                                                "username": "b", "password": "12345"})
            
            assert(resp2.status_code == 200)
            reciever_id = resp2.json['id']
            
            #sending friend requests here-------------------------------

            f_req = client.post('/friendships/send_request', json={
                "sender_id": sender_id,
                "reciever_id": reciever_id
            })

            f_req_oppo = client.post('/friendships/send_request', json={
                "sender_id": reciever_id,
                "reciever_id": sender_id
            })

            reciever = client.get(f"/user_test/{reciever_id}")
            sender = client.get(f"/user_test/{sender_id}")

            assert(sender.status_code == 200)
            assert(f_req.status_code == 200)
            assert(reciever.status_code == 200)
            assert(f_req_oppo.status_code == 200)

            sender_notification_id = sender.json['friend_request_notifications'][0]['id']
            reciever_notification_id = reciever.json['friend_request_notifications'][0]['id']

            #accepts friend request here-----------------------------------

            f_req_oppo_patched = client.patch('/friendships/send_request', json={
                "friend_request_id": f_req_oppo.json['id'],
                "friend_request_response": "accepted"
            })

            assert(f_req_oppo_patched.status_code == 200)
            assert(f_req_oppo_patched.json['_status'] == "accepted")

            f_req_id = f_req.json['id']
            f_req_updated = client.get(f'/friendship_test/{f_req_id}')
            assert(f_req_updated.status_code == 404)

            #check notifications here----------------------------------------

            sender_notification = client.get(f'/friend_request_notification_test/{sender_notification_id}')
            reciever_notification = client.get(f'/friend_request_notification_test/{reciever_notification_id}')

            assert(sender_notification.status_code == 404)
            assert(reciever_notification.status_code == 404)

    def test_dual_friendship_reject(self):
        '''When both users send each other friend requests
        and if one rejected, all friendships and notifications
        are deleted'''

        with app.app_context():
            reset_all()

        with app.test_client() as client:
            #creating accounts here ---------------------------------

            resp1 = client.post("/test_create_an_account", json={"first_name": "a", "last_name": "a",
                                                                "username": "a", "password": "12345"})
            
            assert(resp1.status_code == 200)
            sender_id = resp1.json['id']

            resp2 = client.post("/test_create_an_account", json={"first_name": "b", "last_name": "b",
                                                                "username": "b", "password": "12345"})
            
            assert(resp2.status_code == 200)
            reciever_id = resp2.json['id']
            
            #sending friend requests here-------------------------------

            f_req = client.post('/friendships/send_request', json={
                "sender_id": sender_id,
                "reciever_id": reciever_id
            })
            f_req_id = f_req.json['id']

            f_req_oppo = client.post('/friendships/send_request', json={
                "sender_id": reciever_id,
                "reciever_id": sender_id
            })
            f_req_oppo_id = f_req_oppo.json['id']

            reciever = client.get(f"/user_test/{reciever_id}")
            sender = client.get(f"/user_test/{sender_id}")

            assert(sender.status_code == 200)
            assert(f_req.status_code == 200)
            assert(reciever.status_code == 200)
            assert(f_req_oppo.status_code == 200)

            sender_notification_id = sender.json['friend_request_notifications'][0]['id']
            reciever_notification_id = reciever.json['friend_request_notifications'][0]['id']

            #accepts friend request here-----------------------------------

            client.patch('/friendships/send_request', json={
                "friend_request_id": f_req_oppo.json['id'],
                "friend_request_response": "rejected"
            })

            sender_friendship = client.get(f'/friendship_test/{f_req_id}')
            reciever_friendship = client.get(f'/friendship_test/{f_req_oppo_id}')

            assert(sender_friendship.status_code == 404)
            assert(reciever_friendship.status_code == 404)

            #check notifications here----------------------------------------

            sender_notification = client.get(f'/friend_request_notification_test/{sender_notification_id}')
            reciever_notification = client.get(f'/friend_request_notification_test/{reciever_notification_id}')

            assert(sender_notification.status_code == 404)
            assert(reciever_notification.status_code == 404)

    def test_post_submital(self):
        '''POSTing a social media posts automatically adds 
        it to the database'''

        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            db.session.add_all([u1,u2])
            db.session.commit()

            friendship = u1.send_friend_request(u2.id)
            u2.respond_to_friend_request(friendship.id, "accepted")

        with app.test_client() as client:

            #logs in 
            poster_logged_in = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })

            assert(poster_logged_in.status_code == 200)

            post = client.post("/post_test", json={
                "user_id": poster_logged_in.json['id'],
                "caption": "testing testing"
            })

            #checks if the post has been posted
            assert(post.status_code == 200)

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)

            #logs in with different account
            watcher_logged_in = client.post('/login', json={
                "username": "b",
                "password": "12345"
            })
            assert(watcher_logged_in.status_code == 200)

            watcher_post_feed = client.get('/posts')
            assert(watcher_post_feed.status_code == 200)
            assert(post.json in watcher_post_feed.json)

    def test_post_edit(self):
        '''PATCHing a post works'''
        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            db.session.add_all([u1,u2])
            db.session.commit()

        with app.test_client() as client:
            #logs in 
            poster_logged_in = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })

            assert(poster_logged_in.status_code == 200)
            user_id = poster_logged_in.json['id']

            #creates post
            post = client.post('/post_test', json={
                "user_id": user_id,
                "caption": "testing testing"
            })

            assert(post.status_code == 200)
            post_id = post.json['id']

            #edits post
            editted_post = client.patch(f'/post/{post_id}', json={
                "caption": "patched"
            })

            assert(editted_post.json["caption"] == "patched")
    
    def test_post_like_dislike(self):
        '''When a post is liked, it will create a postlike notification
        for the user who posted the post. However, the postlike notification will
        not pop up if the poster likes his/her own post. And the post like count that
        is identified as isLiked=True will increase in length'''

        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            db.session.add_all([u1,u2])
            db.session.commit()

            friendship = u1.send_friend_request(u2.id)
            u2.respond_to_friend_request(friendship.id, "accepted")

        with app.test_client() as client:

            #logs in 
            poster = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })

            assert(poster.status_code == 200)

            post = client.post("/post_test", json={
                "user_id": poster.json['id'],
                "caption": "testing testing"
            })
            #checks if the post has been posted
            assert(post.status_code == 200)
            post_id = post.json['id']

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)


            #logs in 
            liker = client.post('/login', json={
                "username": "b",
                "password": "12345"
            })

            assert(liker.status_code == 200)
            user_id = liker.json['id']

            #likes post
            post_like = client.post('/post/like', json={
                "isLiked": True,
                "user_id": user_id,
                "post_id": post_id
            })
            post_like_id = post_like.json["id"]
            assert(post_like.status_code == 200)
            assert(post_like.json['id'])

            #see if postLikeNotification exists
            post_like_notifications = client.get('/pln_test')
            assert(post_like_notifications.status_code == 200)
            assert(post_like_notifications.json[0]['id'])
            #checks if a dual notification was created
            assert(len(post_like_notifications.json) == 1)

            post_dislike = client.delete(f'/post/like/{post_like_id}')

            assert(post_dislike.status_code == 204)

    def test_comment(self):
        '''When a comment is made on a post, it will
        create a comment notification for the person who
        posted. And obviously, after the comment, the comment will
        show up on the database'''

        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            db.session.add_all([u1,u2])
            db.session.commit()

            friendship = u1.send_friend_request(u2.id)
            u2.respond_to_friend_request(friendship.id, "accepted")

        with app.test_client() as client:
            #logs in 
            poster = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })

            assert(poster.status_code == 200)

            post = client.post("/post_test", json={
                "user_id": poster.json['id'],
                "caption": "testing testing"
            })
            #checks if the post has been posted
            assert(post.status_code == 200)
            post_id = post.json['id']

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)


            #logs in 
            commenter = client.post('/login', json={
                "username": "b",
                "password": "12345"
            })

            assert(commenter.status_code == 200)
            user_id = commenter.json['id']

            #comments
            comment = client.post("/comment", json={
                "text": "testing comment",
                "user_id": user_id,
                "post_id": post_id
            })

            assert(comment.status_code == 200)
            assert(comment.json['text'] == 'testing comment')

            comment_notifications = client.get('/cn_test')

            assert(comment_notifications.status_code == 200)
            assert(len(comment_notifications.json) == 1)

    def test_comment_patch(self):
        '''When PATCH request for comment arrives,
        it is able to edit it'''

        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            db.session.add_all([u1,u2])
            db.session.commit()

            friendship = u1.send_friend_request(u2.id)
            u2.respond_to_friend_request(friendship.id, "accepted")

        with app.test_client() as client:
            #logs in 
            poster = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })

            assert(poster.status_code == 200)

            post = client.post("/post_test", json={
                "user_id": poster.json['id'],
                "caption": "testing testing"
            })
            #checks if the post has been posted
            assert(post.status_code == 200)
            post_id = post.json['id']

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)


            #logs in 
            commenter = client.post('/login', json={
                "username": "b",
                "password": "12345"
            })

            assert(commenter.status_code == 200)
            user_id = commenter.json['id']

            #comments
            comment = client.post("/comment", json={
                "text": "testing comment",
                "user_id": user_id,
                "post_id": post_id
            })
            comment_id = comment.json['id']
            assert(comment.status_code == 200)
            assert(comment.json['text'] == 'testing comment')

            editted_comment = client.patch(f"/comment/{comment_id}", json={
                "text": "editted comment"
            })
            assert(editted_comment.status_code == 200)
            assert(editted_comment.json["text"] == "editted comment")

    def test_comment_like_dislike(self):
        '''Comment like will obviously create a comment like object
        and also create a comment like notification object only for
        the reciever of the comment like'''

        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            u2 = User(first_name="b", last_name="b", username="b")
            u2.password_hash = "12345"
            u3 = User(first_name="c", last_name="c", username="c")
            u3.password_hash = "12345"
            db.session.add_all([u1,u2,u3])
            db.session.commit()

            f1 = u1.send_friend_request(u2.id)
            f2 = u1.send_friend_request(u3.id)
            f3 = u2.send_friend_request(u3.id)

            u2.respond_to_friend_request(f1.id, "accepted")
            u3.respond_to_friend_request(f2.id, "accepted")
            u3.respond_to_friend_request(f3.id, "accepted")

        with app.test_client() as client:
            #logs in 
            poster = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })
            poster_id = poster.json['id']

            assert(poster.status_code == 200)

            post = client.post("/post_test", json={
                "user_id": poster.json['id'],
                "caption": "testing testing"
            })
            #checks if the post has been posted
            assert(post.status_code == 200)
            post_id = post.json['id']

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)

            #logs in to commenter
            commenter = client.post('/login', json={
                "username": "b",
                "password": "12345"
            })

            assert(commenter.status_code == 200)
            commenter_id = commenter.json['id']

            #comments
            comment = client.post("/comment", json={
                "text": "testing comment",
                "user_id": commenter_id,
                "post_id": post_id
            })
            comment_id = comment.json['id']
            assert(comment.status_code == 200)
            assert(comment.json['text'] == 'testing comment')

            comment_like = client.post("/comment/like", json={
                "user_id": commenter_id,
                "comment_id": comment_id,
                "isLiked": True
            })

            assert(comment_like.status_code == 200)

            commenter = client.get(f'/user_test/{commenter_id}')
            poster = client.get(f'/user_test/{poster_id}')
            commenter_cln = commenter.json['comment_like_notifications']
            poster_cln = poster.json['comment_like_notifications']

            assert(len(commenter_cln) == 0)
            assert(len(poster_cln) == 1)

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)

            #login to poster
            poster = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })
            poster_id = poster.json['id']

            assert(poster.status_code == 200)

            comment_like = client.post("/comment/like", json={
                "user_id": poster_id,
                "comment_id": comment_id,
                "isLiked": True
            })
            assert(comment_like.status_code == 200)

            commenter = client.get(f'/user_test/{commenter_id}')
            poster = client.get(f'/user_test/{poster_id}')
            commenter_cln = commenter.json['comment_like_notifications']
            poster_cln = poster.json['comment_like_notifications']

            assert(len(commenter_cln) == 1)
            assert(len(poster_cln) == 1)

            #logs out
            resp = client.delete("/logout")
            assert(resp.status_code == 204)
            
            #login to 3rd party
            rando = client.post('/login', json={
                "username": "c",
                "password": "12345"
            })
            rando_id = rando.json['id']

            assert(rando.status_code == 200)

            comment_like = client.post("/comment/like", json={
                "user_id": rando_id,
                "comment_id": comment_id,
                "isLiked": True
            })
            assert(comment_like.status_code == 200)

            commenter = client.get(f'/user_test/{commenter_id}')
            poster = client.get(f'/user_test/{poster_id}')
            rando = client.get(f'/user_test/{rando_id}')
            commenter_cln = commenter.json['comment_like_notifications']
            poster_cln = poster.json['comment_like_notifications']
            rando_cln = rando.json['comment_like_notifications']

            print(rando_cln)

            assert(len(rando_cln) == 0)
            assert(len(commenter_cln) == 2)
            assert(len(poster_cln) == 2)

    def test_user_delete(self):
        '''Checks if user is removed and logged out
        after deletion. And user profile picture and post pictures
        directory must be deleted'''
        
        with app.app_context():
            reset_all()
            u1 = User(first_name="a", last_name="a", username="a")
            u1.password_hash= "12345"
            db.session.add(u1)
            db.session.commit()

        with app.test_client() as client:

            user = client.post('/login', json={
                "username": "a",
                "password": "12345"
            })
            user_id = user.json['id']

            assert(user.status_code == 200)
            assert(user_id == 1)

            delete_user = client.delete(f"/user_test/delete/{user_id}")
            assert(delete_user.status_code == 204)

            try:
                user_id = flask.session.get('user_id')
                n_of_users = flask.session.get('n_of_users')
                print(user_id, n_of_users)
            except:
                deletedUser = User.query.filter(User.id == user_id).first()
                assert(deletedUser is None)
                assert(True)

            user_pictures_path = f"../client/phase-5-project/public/images/{user_id}_folder"
            assert(os.path.exists(user_pictures_path) == False)













            

            






















            








            


            
















            
            


                
              
