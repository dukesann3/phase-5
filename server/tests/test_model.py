from models import User, Friendship, Notification
from app import app, db
import ipdb

class TestModel:
    def test_check_friendship_uniquness(self):
        '''friendships table must have unique value combinations of 
        sender_id and reciever_id for it to be added into the database'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "t1"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "t2"

            db.session.add_all([u1, u2])
            db.session.commit()

            f1 = Friendship(sender_id=u1.id, reciever_id=u2.id)
            db.session.add(f1)
            db.session.commit()

            f2 = Friendship(sender_id=u1.id, reciever_id=u2.id)
            db.session.add(f2)
            
            try:
                db.session.commit()
                assert False
            except:
                assert True

    def test_check_friendship_status(self):
        '''friendship status must be either accepted, 
        rejected, or pending'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "t1"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "t2"

            db.session.add_all([u1, u2])
            db.session.commit()

            try:
                f1 = Friendship(sender_id=u1.id, reciever_id=u2.id, _status="booboo")
                db.session.add(f1)
                db.session.commit()
                assert False
            except:
                assert True

    def test_check_dual_friendship(self):
        '''A dual friendship can only exist if the two
        of them are pending. If not, it cannot exist'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "t1"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "t2"

            db.session.add_all([u1, u2])
            db.session.commit()

            f1 = Friendship(sender_id=u1.id, reciever_id=u2.id)
            f2 = Friendship(sender_id=u2.id, reciever_id=u1.id)
            db.session.add_all([f1, f2])
            db.session.commit()

            assert f1._status == "pending"
            assert f2._status == "pending"

            try:
                f1.status = "accepted"
                assert False
            except:
                assert True

    def test_notification_uniqueness(self):
        '''Notification must have unique sender, reciever,
        text, and type'''
        with app.app_context():
            Friendship.query.delete()
            Notification.query.delete()
            User.query.delete()
            db.session.commit()

            u1 = User(first_name="t1", last_name="t2", username="tt1")
            u1.password_hash = "t1"
            u2 = User(first_name="t2", last_name="t2", username="tt2")
            u2.password_hash = "t2"
            
            db.session.add_all([u1, u2])
            db.session.commit()

            n1 = Notification(notification_sender_id=u1.id, notification_reciever_id=u2.id,
                              text="ABC", notification_type="Friend Request")
            n2 = Notification(notification_sender_id=u1.id, notification_reciever_id=u2.id,
                              text="ABC", notification_type="Friend Request")
            
            try:
                db.session.add_all([n1, n2])
                db.session.commit()
                assert False
            except:
                assert True

    def test_send_friend_request(self):
            '''Tests if friend request will produce a friendship
            row for both request sender and reciever. And sends a notification
            only to the request reciever'''
            with app.app_context():
                Friendship.query.delete()
                Notification.query.delete()
                User.query.delete()
                db.session.commit()

                u1 = User(first_name="t1", last_name="t2", username="tt1")
                u1.password_hash = "t1"
                u2 = User(first_name="t2", last_name="t2", username="tt2")
                u2.password_hash = "t2"

                db.session.add_all([u1, u2])
                db.session.commit()

                u1.send_friend_request(u2.id)

                assert u1.friendships
                assert u2.friendships
                assert not u1.notifications
                assert u2.notifications

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

                u1 = User(first_name="t1", last_name="t2", username="tt1")
                u1.password_hash = "t1"
                u2 = User(first_name="t2", last_name="t2", username="tt2")
                u2.password_hash = "t2"
                
                db.session.add_all([u1, u2])
                db.session.commit()

                friend_request = u1.send_friend_request(u2.id)
                u2.respond_to_friend_request(friend_request.id,"accepted")

                assert u1.friendships[0].status == "accepted"
                assert u2.friendships[0].status == "accepted"
                assert not u1.notifications
                assert not u2.notifications
    


            







            

                

