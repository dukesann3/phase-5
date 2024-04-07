from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
import ipdb

db = SQLAlchemy()

class Friendship(db.Model, SerializerMixin):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id", nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id", nullable=False)
    _status = db.Column(db.Enum("pending", "accepted", "rejected", name="friendship_status"), default="pending")

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="friendships")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="friendships")

    notification = db.relationship("Notification", 
                                    secondary="users",
                                    primaryjoin="or_(Friendship.sender_id == User.id, Friendship.reciever_id == User.id)",
                                    secondaryjoin='''and_(or_(User.id == Notification.notification_sender_id, 
                                    User.id == Notification.notification_reciever_id), Notification.notification_type == 'Friend Request')''',
                                    back_populates="friendship",
                                    viewonly=True)

    serialize_rules = ("-sender.friendships","-reciever.friendships","-notifications.friendships")

    @hybrid_property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if not value in ["pending", "accepted", "rejected"]:
            raise ValueError("Friendship status must be pending, accepted, or rejected.")
        self._status = value

    @validates("sender_id", "reciever_id")
    def validate_ids(self, key, value):
        if key == "reciever_id":
            #find user with same sender id ... self.sender_id is now in the system
            potential_duplicate_friendship = Friendship.query.filter(Friendship.sender_id == self.sender_id and Friendship.reciever_id == value).all()
            oppo_friend_request = Friendship.query.filter(Friendship.reciever_id == self.sender_id and Friendship.sender_id == value).first()

            if self.sender_id == value and key == "reciever_id":
                raise ValueError("Reciever id and Sender id must be a different value from each other. A user cannot friend him/herself.")
            elif potential_duplicate_friendship:
                raise ValueError("There cannot be duplicate friendship")
            elif oppo_friend_request:
                try:
                    if oppo_friend_request.status == "pending":
                        raise ValueError("A two way friend request cannot have one request have anything other than pending")
                except:
                    return 
                return value     
        elif key == "sender_id":
            return value
        return value

    def __repr__(self):
        return f'Sender ID: {self.sender_id}, Reciever ID: {self.reciever_id}, Status: {self._status}'
    
class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    notification_sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_sender_id", nullable=False)
    notification_reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_reciever_id", nullable=False)
    text = db.Column(db.String, nullable=False)
    notification_type = db.Column(db.Enum("Friend Request", "Comment", "Message", "Like", name="notification_type"), default="Friend Request")

    notification_sender = db.relationship("User", foreign_keys=[notification_sender_id], back_populates="notifications")
    notification_reciever = db.relationship("User", foreign_keys=[notification_reciever_id], back_populates="notifications")

    friendship = db.relationship("Friendship", 
                                    secondary="users",
                                    primaryjoin='''or_(and_(Notification.notification_sender_id == User.id, Notification.notification_reciever_id == User.id),
                                    (Notification.notification_type == 'Friend Request'))''',
                                    secondaryjoin="or_(User.id == Friendship.sender_id, User.id == Friendship.reciever_id)",
                                    back_populates="notification",
                                    viewonly=True)

    def __repr__(self):
        return f'request type: {self.notification_type} sender ID: {self.notification_sender_id} reciever ID: {self.notification_reciever_id}'


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    friendships = db.relationship(
        "Friendship",
        primaryjoin="or_(User.id == Friendship.reciever_id, User.id == Friendship.sender_id)"
    )

    notifications = db.relationship(
        "Notification",
        primaryjoin="(User.id == Notification.notification_reciever_id)"
    )

    @hybrid_property
    def friends(self):
        friends = []
        for friendship in self.friendships:
            if not self.id == friendship.reciever_id and friendship.status == "accepted":
                friends.append(friendship.reciever)
            elif not self.id == friendship.sender_id and friendship.status == "accepted":
                friends.append(friendship.sender)

        return friends
    
    #potential friend is an id since it is not so important since you want a lot of friends
    @hybrid_method
    def send_friend_request(self, potential_friend_id):
        friendship = Friendship(sender_id=self.id, reciever_id=potential_friend_id)
        notification = Notification(notification_sender_id=self.id, notification_reciever_id=potential_friend_id,
                                    text=f"{self.name} wants to be friends with you",notification_type="Friend Request")
        db.session.add_all([friendship, notification])
        db.session.commit()

    #friend request not in id form since it must be a specific friend request
    @hybrid_method
    def respond_to_friend_request(self, friend_request, response):
        if not response in ["accepted", "rejected"]:
            print(response)
            raise ValueError("Response must be either accepted or rejected")
        
        if response == "accepted":
            friend_request.status = response
            db.session.add(friend_request)
            notification = friend_request.notification[0]
            db.session.delete(notification)
        elif response == "rejected":
            notification = friend_request.notification[0]
            db.session.delete(friend_request)
            db.session.delete(notification)
            
    serialize_rules = ("-friendships.sender","-friendships.reciever", "-notifications.notification_sender", "-notifications.notification_reciever","-friendships.notifications")

    def __repr__(self):
        return f'username: {self.name}'
    

    



    

    



        

    











