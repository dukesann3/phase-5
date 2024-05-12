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

    post_like_notifications = db.relationship("PostLikeNotification", back_populates="post")

    @hybrid_property
    def image_src(self):
        return self._image_src
    
    @image_src.setter
    def image_src(self, image_src):
        if not isinstance(image_src, str):
            raise TypeError("Image URI must be in string format")
        
        self._image_src = image_src

    serialize_rules = ("-user",
                       "-post_like_notifications.sender", "-post_like_notifications.reciever", "-post_like_notifications.post",
                       "-comments.comment_like_notifications")

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

    serialize_rules = ("-user","-post")

class PostLikeNotification(db.Model, SerializerMixin):
    __tablename__ = "post_like_notifications"
    __table_args__ = (
        db.CheckConstraint("sender_id != reciever_id", name="sender_reciever_uniqueness"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id", nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id", nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="post_like_notifications")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="post_like_notifications")
    post = db.relationship("Post", foreign_keys=[post_id], back_populates="post_like_notifications")

    serialize_rules = ("-sender", "-receiver", 
                       "-post.user", "-post.comments", "-post.post_like_notifications")
    
    @validates("sender_id", "reciever_id")
    def validate_users(self, key, user_id):
        if key == "sender_id":
            return user_id
        elif key == "reciever_id":
            if self.sender_id == user_id:
                raise ValueError("Cannot have post like notification for yourself")
            else:
                return user_id



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
    comment_notification = db.relationship("CommentNotification", back_populates="comment")
    comment_likes = db.relationship("CommentLike", back_populates="comment")
    comment_like_notifications = db.relationship("CommentLikeNotification", back_populates="comment")

    serialize_rules = ("-post","-user",
                       "-comment_notification.sender", "-comment_notification.reciever","-comment_notification.comment",
                       "-comment_likes.sender", "-comment_likes.reciever", "-comment_likes.comment",
                       "-comment_like_notifications.sender", "-comment_like_notifications.reciever", "-comment_like_notifications.comment")

class CommentNotification(db.Model, SerializerMixin):
    __tablename__ = "comment_notifications"
    __table_args__ = (
        db.CheckConstraint("sender_id != reciever_id", name="sender_reciever_uniqueness"),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)
    text = db.Column(db.String, nullable=False)

    comment = db.relationship("Comment", foreign_keys=[comment_id], back_populates="comment_notification")
    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="comment_notifications")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="comment_notifications")

    serialize_rules = ("-user", "-comment")

    @validates("sender_id", "reciever_id")
    def validate_users(self, key, user_id):
        if key == "sender_id":
            return user_id
        elif key == "reciever_id":
            if self.sender_id == user_id:
                raise ValueError("Cannot have comment notification for yourself")
            else:
                return user_id

class CommentLike(db.Model, SerializerMixin):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key=True)
    isLiked = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)

    user = db.relationship("User", back_populates="comment_like")
    comment = db.relationship("Comment", back_populates="comment_likes")

    serialize_rules = ("-user", "-comment")

class CommentLikeNotification(db.Model, SerializerMixin):
    __tablename__ = "comment_like_notifications"
    __table_args__ = (
        db.CheckConstraint("sender_id != reciever_id", name="sender_reciever_uniqueness"),
    )

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id", nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id", nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="comment_like_notifications")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="comment_like_notifications")
    comment = db.relationship("Comment", foreign_keys=[comment_id], back_populates="comment_like_notifications")

    @validates("sender_id", "reciever_id")
    def validate_users(self, key, user_id):
        if key == "sender_id":
            return user_id
        elif key == "reciever_id":
            if self.sender_id == user_id:
                raise ValueError("Cannot have comment like notification for yourself")
            else:
                return user_id

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

    friend_request_notification = db.relationship("FriendRequestNotification", 
                                    secondary="users",
                                    primaryjoin="or_(Friendship.sender_id == User.id, Friendship.reciever_id == User.id)",
                                    secondaryjoin='''or_(User.id == FriendRequestNotification.sender_id, 
                                    User.id == FriendRequestNotification.reciever_id)''',
                                    back_populates="friendship",
                                    viewonly=True)

    serialize_rules = ("-sender.friendships","-reciever.friendships","-friend_request_notification.friendship", 
                       "-friend_request_notification.sender", "-friend_request_notification.reciever",
                       "-sender.friend_request_notifications", "-reciever.friend_request_notifications")

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
    
class FriendRequestNotification(db.Model, SerializerMixin):
    __tablename__ = "friend_request_notifications"
    __table_args__ = (
        db.UniqueConstraint("sender_id", "reciever_id",
                            "text", name="notification_uniqueness"),
    )

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="sender_id", nullable=False)
    reciever_id = db.Column(db.Integer, db.ForeignKey("users.id"), name="reciever_id", nullable=False)
    friendship_id = db.Column(db.Integer, db.ForeignKey("friendships.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="friend_request_notifications")
    reciever = db.relationship("User", foreign_keys=[reciever_id], back_populates="friend_request_notifications")

    friendship = db.relationship("Friendship", 
                                    secondary="users",
                                    primaryjoin='''or_(FriendRequestNotification.sender_id == User.id, FriendRequestNotification.reciever_id == User.id)''',
                                    secondaryjoin="or_(User.id == Friendship.sender_id, User.id == Friendship.reciever_id)",
                                    back_populates="friend_request_notification",
                                    viewonly=True)
    
    serialize_rules = ("-sender","-reciever",
                       "-friendship.sender", "-friendship.reciever", "-friendship.friend_request_notification")

    def __repr__(self):
        return f'sender ID: {self.sender_id} reciever ID: {self.reciever_id}'


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
        primaryjoin="or_(User.id == Friendship.reciever_id, User.id == Friendship.sender_id)",
        cascade="all, delete"
    )

    friend_request_notifications = db.relationship(
        "FriendRequestNotification",
        primaryjoin="(User.id == FriendRequestNotification.reciever_id)",
        cascade="all, delete"
    )

    posts = db.relationship("Post", back_populates="user", cascade="all, delete")
    comments = db.relationship("Comment", back_populates="user", cascade="all, delete")
    post_like = db.relationship("PostLike", back_populates="user", cascade="all, delete")
    comment_like = db.relationship("CommentLike", back_populates="user", cascade="all, delete")

    post_like_notifications = db.relationship(
        "PostLikeNotification",
        primaryjoin="(User.id == PostLikeNotification.reciever_id)",
        cascade="all, delete"
    )

    comment_like_notifications = db.relationship(
        "CommentLikeNotification",
        primaryjoin="(User.id == CommentLikeNotification.reciever_id)",
        cascade="all, delete"
    )

    comment_notifications = db.relationship(
        "CommentNotification",
        primaryjoin="(User.id == CommentNotification.reciever_id)",
        cascade="all, delete"
    )

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
    
    @hybrid_property
    def pending_friends(self):
        pending_friends = []
        for friendship in self.friendships:
            if not self.id == friendship.reciever_id and friendship.status == "pending":
                pending_friends.append(friendship)
        
        return pending_friends
    
    
    @hybrid_method
    def send_friend_request(self, potential_friend_id):

        friendship = Friendship(sender_id=self.id, reciever_id=potential_friend_id)
        db.session.add(friendship)
        db.session.commit()
        friend_request_notification = FriendRequestNotification(sender_id=self.id, reciever_id=potential_friend_id, friendship_id=friendship.id,
                                    text=f"{self.first_name} wants to be friends with you")
        db.session.add(friend_request_notification)
        db.session.commit()
        return friendship


    @hybrid_method
    def respond_to_friend_request(self, friend_request_id, response):
        if not response in ["accepted", "rejected"]:
            raise ValueError("Response must be either accepted or rejected")
        
        f = Friendship.query.filter(Friendship.id == friend_request_id).first()
        n = FriendRequestNotification.query.filter(FriendRequestNotification.sender_id == f.sender_id and FriendRequestNotification.reciever_id == self.id).first()
        #must delete opposite friend request it is a two way friend request before accepting or rejecting
        oppo_f = Friendship.query.filter(Friendship.sender_id == f.reciever_id and Friendship.reciever_id == f.sender_id).first()
        oppo_n = FriendRequestNotification.query.filter(FriendRequestNotification.sender_id == self.id and FriendRequestNotification.reciever_id == f.sender_id).first()

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
                        "-friend_request_notifications.reciever", "-friend_request_notifications.sender",
                        "-friend_request_notifications.friendship.sender","-friend_request_notifications.friendship.reciever","-friend_request_notifications.friendship.friend_request_notification", 
                        "-friendships.reciever", "-friendships.sender", "-friendships.friend_request_notification",
                        "-post_like_notifications.sender", "-post_like_notifications.reciever", "-post_like_notifications.post",
                        "-comment_notifications.sender", "-comment_notifications.reciever", "-comment_notifications.comment",
                        "-comment_like_notifications.sender", "-comment_like_notifications.reciever", "-comment_like_notifications.comment")

    def __repr__(self):
        return f'username: {self.first_name}, friendships: {self.friendships}'
    

    



    

    



        

    











