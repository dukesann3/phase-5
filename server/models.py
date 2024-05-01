from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from configs import bcrypt, db
import ipdb
import urllib.request
import os

class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    _image_src = db.Column(db.String)
    location = db.Column(db.String)
    caption = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")
    post_likes = db.relationship("PostLike", back_populates="post")

    @hybrid_property
    def image_src(self):
        return self._image_src
    
    @image_src.setter
    def image_src(self, image_src):
        if not isinstance(image_src, str):
            raise TypeError("Image URI must be in string format")
        
        self._image_src = image_src


    serialize_rules = ("-user","-post_likes")

class PostLike(db.Model, SerializerMixin):
    __tablename__ = "postlikes"

    id = db.Column(db.Integer, primary_key=True)
    isLiked = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    user = db.relationship("User", back_populates="post_like")
    post = db.relationship("Post", back_populates="post_likes")

    serialize_rules = ("user","post")

class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    user = db.relationship("User", back_populates="comments")
    post = db.relationship("Post", back_populates="comments")
    comment_likes = db.relationship("CommentLike", back_populates="comment")

    serialize_rules = ("-post","-user", "-comment_likes")

class CommentLike(db.Model, SerializerMixin):
    __tablename__ = "commentlikes"

    id = db.Column(db.Integer, primary_key=True)
    isLiked = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)

    user = db.relationship("User", back_populates="comment_like")
    comment = db.relationship("Comment", back_populates="comment_likes")

    serialize_rules = ("-user", "-comment")



class Friendship(db.Model, SerializerMixin):
    __tablename__ = "friendships"
    __table_args__ = (
        db.UniqueConstraint("sender_id", "reciever_id", name="unique_foreign_keys"),
    )

    #not sure if check constraint is working, but one of them prevents same key from being put in the db.
    #dual friendships may exist as long as the requests are pending. If not, then that is a problem.

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id", nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id", nullable=False)
    _status = db.Column(db.Enum("pending", "accepted", "rejected", name="friendship_status"), default="pending")

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="friendships")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="friendships")

    notification = db.relationship("Notification", 
                                    secondary="users",
                                    primaryjoin="or_(Friendship.sender_id == User.id, Friendship.reciever_id == User.id)",
                                    secondaryjoin='''and_(or_(User.id == Notification.notification_sender_id, 
                                    User.id == Notification.notification_reciever_id), Notification.notification_type == 'Friend Request')''',
                                    back_populates="friendship",
                                    viewonly=True)

    serialize_rules = ("-sender.friendships","-reciever.friendships","-notification.friendship", 
                       "-notification.notification_sender", "-notification.notification_reciever",
                       "-sender.notifications", "-reciever.notifications")

    @hybrid_property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        sender_id = self.sender_id
        reciever_id = self.reciever_id

        opposite_friend_request = Friendship.query.filter(Friendship.sender_id == reciever_id and Friendship.reciever_id == sender_id).first()
        if not value in ["pending", "accepted", "rejected"]:
            raise ValueError("Friendship status must be pending, accepted, or rejected.")
        elif opposite_friend_request:
            if opposite_friend_request._status != value:
                raise ValueError('''With a two way friend request, it cannot have one request that is pending
                                 where the other being accepted or rejected. You will need to 
                                 delete the sender's request, then update it to either accepted or rejected''')
        self._status = value
        
    @validates("sender_id", "reciever_id")
    def validate_ids(self, key, value):
        if key == "reciever_id":
            if self.sender_id == value:
                raise ValueError("Sender and reciever for a friendship request cannot be the same person.")
        elif key == "sender_id":
            return value
        return value

    def __repr__(self):
        return f'Sender ID: {self.sender_id}, Reciever ID: {self.reciever_id}, Status: {self._status}'
    
class Notification(db.Model, SerializerMixin):
    __tablename__ = "notifications"
    __table_args__ = (
        db.UniqueConstraint("notification_sender_id", "notification_reciever_id",
                            "text", "notification_type", name="notification_uniqueness"),
    )

    id = db.Column(db.Integer, primary_key=True)
    notification_sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_sender_id", nullable=False)
    notification_reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="notification_reciever_id", nullable=False)
    text = db.Column(db.String, nullable=False)
    notification_type = db.Column(db.Enum("Friend Request", "Comment", "Message", "Like", name="notification_type"), default="Friend Request")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    notification_sender = db.relationship("User", foreign_keys=[notification_sender_id], back_populates="notifications")
    notification_reciever = db.relationship("User", foreign_keys=[notification_reciever_id], back_populates="notifications")

    friendship = db.relationship("Friendship", 
                                    secondary="users",
                                    primaryjoin='''and_(or_(Notification.notification_sender_id == User.id, Notification.notification_reciever_id == User.id),
                                    (Notification.notification_type == 'Friend Request'))''',
                                    secondaryjoin="or_(User.id == Friendship.sender_id, User.id == Friendship.reciever_id)",
                                    back_populates="notification",
                                    viewonly=True)
    
    serialize_rules = ("-notification_sender","-notification_reciever",
                       "-friendship.sender", "-friendship.reciever", "-friendship.notification")

    def __repr__(self):
        return f'request type: {self.notification_type} sender ID: {self.notification_sender_id} reciever ID: {self.notification_reciever_id}'


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.Integer, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    _image_src = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    friendships = db.relationship(
        "Friendship",
        primaryjoin="or_(User.id == Friendship.reciever_id, User.id == Friendship.sender_id)"
    )

    notifications = db.relationship(
        "Notification",
        primaryjoin="(User.id == Notification.notification_reciever_id)",
    )

    posts = db.relationship("Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    post_like = db.relationship("PostLike", back_populates="user")
    comment_like = db.relationship("CommentLike", back_populates="user")

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if len(password) < 5:
            raise ValueError("Password must be at least 5 letters")
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    @hybrid_property
    def image_src(self):
        return self._image_src
    
    @image_src.setter
    def image_src(self, image_src):
        if not isinstance(image_src, str):
            raise TypeError("Image src must be a string. In other words, image URI.")
        self._image_src = image_src

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    @hybrid_property
    def friends(self):
        friends = []
        for friendship in self.friendships:
            if not self.id == friendship.reciever_id and friendship.status == "accepted":
                friends.append(friendship.reciever)
            elif not self.id == friendship.sender_id and friendship.status == "accepted":
                friends.append(friendship.sender)

        return friends
    
    @hybrid_method
    def send_friend_request(self, potential_friend_id):

        friendship = Friendship(sender_id=self.id, reciever_id=potential_friend_id)
        notification = Notification(notification_sender_id=self.id, notification_reciever_id=potential_friend_id,
                                    text=f"{self.first_name} wants to be friends with you", notification_type="Friend Request")
        db.session.add_all([friendship, notification])
        db.session.commit()
        return friendship


    @hybrid_method
    def respond_to_friend_request(self, friend_request_id, response):
        if not response in ["accepted", "rejected"]:
            raise ValueError("Response must be either accepted or rejected")
        
        f = Friendship.query.filter(Friendship.id == friend_request_id).first()
        n = Notification.query.filter(Notification.notification_sender_id == f.sender_id and Notification.notification_reciever_id == self.id and Notification.notification_type == "Friend Request").first()
        #must delete opposite friend request it is a two way friend request before accepting or rejecting
        oppo_f = Friendship.query.filter(Friendship.sender_id == f.reciever_id and Friendship.reciever_id == f.sender_id).first()
        oppo_n = Notification.query.filter(Notification.notification_sender_id == self.id and Notification.notification_reciever_id == f.sender_id and Notification.notification_type == "Friend Request").first()

        if oppo_f:
            if not oppo_f.status == response:
                db.session.delete(oppo_n)
                db.session.delete(oppo_f)
                db.session.commit()
        
        if response == "accepted":
            f.status = response
            db.session.add(f)
            db.session.commit()
            db.session.delete(n)
            db.session.commit()
        elif response == "rejected":
            db.session.delete(n)
            db.session.commit()
            db.session.delete(f)
            db.session.commit()

            
    # serialize_rules = ("-friendships.reciever","-friendships.sender", "-notifications.notification_sender"
    #                    , "-notifications.notification_reciever", "-notifications.friendship", "-friendships.notification"
    #                    , "-posts.user", "-posts.comments","-comments.user","-comments.post")

    serialize_rules = ("-comments", "-posts", "-_password_hash",
                        "-post_like", "-comment_like",
                        "-notifications.notification_reciever", "-notifications.notification_sender",
                        "-notifications.friendship.sender","-notifications.friendship.reciever","-notifications.friendship.notification", 
                        "-friendships.reciever", "-friendships.sender", "-friendships.notification")

    def __repr__(self):
        return f'username: {self.first_name}, friendships: {self.friendships}'
    

    



    

    



        

    











