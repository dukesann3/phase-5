from models import User, Friendship, FriendRequestNotification, Post, PostLike, PostLikeNotification, Comment, CommentLike, CommentNotification, CommentLikeNotification
from configs import db, cache
from app import app

def restart_database():
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
    cache.clear()
    db.session.commit()



