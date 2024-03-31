from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    friendships = db.relationship("Friendship",
                                primaryjoin="or_(User.id == Friendship.user1_id, User.id == Friendship.user2_id)")
    
    serialize_rules = ("-friendships.user1","-friendships.user2")

    def __repr__(self):
        return f'username: {self.name}'


class Friendship(db.Model, SerializerMixin):
    __tablename__ = "friendships"

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    _status = db.Column(db.Enum("pending", "accepted", "rejected", name="friendship_status"), default="pending")

    user1 = db.relationship("User", back_populates="friendships", foreign_keys=[user1_id])
    user2 = db.relationship("User", back_populates="friendships", foreign_keys=[user2_id])

    serialize_rules = ("user1.friendships","user2.friendships")

    @hybrid_property
    def users(self):
        return [self.user1, self.user2]

    @hybrid_property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        if not value in ["pending, accepted, rejected"]:
            raise ValueError("Friendship status must be pending, accepted, or rejected.")
        self._status = value

    @hybrid_property
    def friend_of(self, user_id):
        return self.users[0] if self.users[0].id != user_id else self.users[1]
    
    def __repr__(self):
        return f'User1 ID: {self.user1_id}, User2 ID: {self.user2_id}'
    

    



        

    











