from models import User, Friendship, Notification
from app import app, db
import ipdb

class TestApp:
    def test_creating_new_user(self):
        pass

    def test_send_friend_request(self):
        '''Tests if friend request will produce a friendship
        row for both request sender and reciever. And sends a notification
        only to the request reciever'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(name="t1")
            u2 = User(name="t2")
            db.session.add_all([u1, u2])
            db.session.commit()

            response = app.test_client().post('/friendships/send_request',
                                              json={
                                                  "sender_id": u1.id,
                                                  "reciever_id": u2.id
                                              })

            created_friend_request = Friendship.query.filter(Friendship.sender_id == u1.id and Friendship.reciever_id == u2.id).first()

            assert created_friend_request.to_dict() == response.json
            assert response.status_code == 200
            assert response.content_type == 'application/json'

    def test_accept_friend_request(self):
        '''When friend request is accepted, the friend request
         row will change its status from pending to accepted. And 
         simultaneously delete notification from the request reciever
         regarding the friend request'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(name="t1")
            u2 = User(name="t2")
            db.session.add_all([u1, u2])
            db.session.commit()

            friend_request = u1.send_friend_request(u2.id)

            response = app.test_client().patch('/friendships/send_request',
                                               json={
                                                   "friend_request_id": friend_request.id,
                                                   "friend_request_response": "accepted"
                                               })
            
            assert response.status_code == 200
            assert response.json == friend_request.to_dict()
            assert friend_request.status == "accepted"
            assert not friend_request.notification
            
            


                
              
