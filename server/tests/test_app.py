from models import User, Friendship, Notification
from configs import db
from app import app
from flask import Flask, url_for
import flask
import ipdb

class TestLogAndFriendRequest:

    def test_create_account(self):
        '''Create account works'''

        with app.app_context():
            User.query.delete()
            Friendship.query.delete()
            Notification.query.delete()
            db.session.commit()

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
            User.query.delete()
            Friendship.query.delete()
            Notification.query.delete()
            db.session.commit()

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
            User.query.delete()
            Friendship.query.delete()
            Notification.query.delete()
            db.session.commit()

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
            User.query.delete()
            Friendship.query.delete()
            Notification.query.delete()
            db.session.commit()

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
            assert(len(sender.json['notifications']) == 0)
            assert(bool(reciever.json['notifications'][0]) == True)


    def test_accept_friend_request(self):
        '''When friend request is accepted, the friend request
         row will change its status from pending to accepted. And 
         simultaneously delete notification from the request reciever
         regarding the friend request'''
        
        #check for database entries afterwards
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

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
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

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
            assert(len(sender.json['notifications']) == 0)
            assert(len(reciever.json['notifications']) == 0)

    def test_dual_friendship_accept(self):
        '''When both users send each other friend requests
        and if one accepts, all their notifications are deleted
        and the friendship request which the user accepts will be the
        one that will remain. The other will be deleted'''

        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

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

            sender_notification_id = sender.json['notifications'][0]['id']
            reciever_notification_id = reciever.json['notifications'][0]['id']

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

            sender_notification = client.get(f'/notification_test/{sender_notification_id}')
            reciever_notification = client.get(f'/notification_test/{reciever_notification_id}')

            assert(sender_notification.status_code == 404)
            assert(reciever_notification.status_code == 404)

    def test_dual_friendship_reject(self):
        '''When both users send each other friend requests
        and if one rejected, all friendships and notifications
        are deleted'''

        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

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

            sender_notification_id = sender.json['notifications'][0]['id']
            reciever_notification_id = reciever.json['notifications'][0]['id']

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

            sender_notification = client.get(f'/notification_test/{sender_notification_id}')
            reciever_notification = client.get(f'/notification_test/{reciever_notification_id}')

            assert(sender_notification.status_code == 404)
            assert(reciever_notification.status_code == 404)
















            
            


                
              
