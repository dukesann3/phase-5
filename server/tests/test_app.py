from models import User, Friendship, Notification
from configs import db
from app import app
from flask import Flask, url_for
import flask
import ipdb

class TestApp:

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
        pass
    
    def test_create_account(self):
        pass

    def test_send_friend_request(self):
        '''Tests if friend request will produce a friendship
        row for both request sender and reciever. And sends a notification
        only to the request reciever'''

        #check for database entries afterwards.
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "12345"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "12345"

            db.session.add_all([u1, u2])
            db.session.commit()

            response = app.test_client().post('/friendships/send_request',
                                              json={
                                                  "sender_id": u1.id,
                                                  "reciever_id": u2.id
                                              })

            created_friend_request = Friendship.query.filter(Friendship.sender_id == u1.id and Friendship.reciever_id == u2.id).first()
            print(response)
            assert created_friend_request.to_dict() == response.json
            assert response.status_code == 200
            assert response.content_type == 'application/json'

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

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "12345"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "12345"

            db.session.add_all([u1, u2])
            db.session.commit()

            friend_request = u1.send_friend_request(u2.id)

            response = app.test_client().patch('/friendships/send_request',
                                               json={
                                                   "friend_request_id": friend_request.id,
                                                   "friend_request_response": "accepted"
                                               })
            print(response)
            assert response.status_code == 200
            assert response.json == friend_request.to_dict()
            assert friend_request.status == "accepted"
            assert not friend_request.notification







            
            


                
              
