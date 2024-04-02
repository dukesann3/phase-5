from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
import ipdb

db = SQLAlchemy()

class Friendship(db.Model, SerializerMixin):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id")
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id")
    _status = db.Column(db.Enum("pending", "accepted", "rejected", name="friendship_status"), default="pending")

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="friendships")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="friendships")

    serialize_rules = ("-sender.friendships","-reciever.friendships")

    @hybrid_property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if not value in ["pending, accepted, rejected"]:
            raise ValueError("Friendship status must be pending, accepted, or rejected.")
        self._status = value

    @validates("sender_id", "reciever_id")
    def validate_ids(self, key, value):
        if self.sender_id == value and key == "reciever_id":
            raise ValueError("Reciever id and Sender id must be a different value from each other. A user cannot friend him/herself.")
        elif key == "sender_id":
            return value
        return value
    
    def __repr__(self):
        return f'Sender ID: {self.sender_id}, Reciever ID: {self.reciever_id}'
    
class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    notification_sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_sender_id", nullable=False)
    notification_reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_reciever_id", nullable=False)
    text = db.Column(db.String, nullable=False)
    _notification_type = db.Column(db.Enum("Friend Request", name="notification_type"), default="Friend Request")

    notification_sender = db.relationship("User", foreign_keys=[notification_sender_id], back_populates="notifications")
    notification_reciever = db.relationship("User", foreign_keys=[notification_reciever_id], back_populates="notifications")

    @hybrid_property
    def notification_type(self):
        return self._notification_type

    def __repr__(self):
        return f'request type: {self._notification_type} sender ID: {self.notification_sender_id} reciever ID: {self.notification_reciever_id}'


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
        pass

    serialize_rules = ("-friendships.sender","-friendships.reciever")

    def __repr__(self):
        return f'username: {self.name}'
    

    



    

    



        

    











