# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask import jsonify
import time, datetime

db = SQLAlchemy(use_native_unicode="utf8")

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'router'

class User(UserMixin, db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.String(20), doc='邮箱', primary_key=True)
    nickname = db.Column(db.String(20), doc='昵称', default='微聊用户', nullable=False)
    password_hash = db.Column(db.String(128), doc='密码散列值', nullable=False)
    sex = db.Column(db.String(5), doc='性别', default='未知', nullable=False)
    city = db.Column(db.String(10), doc='城市', default='未知城市', nullable=False)
    signature = db.Column(db.String(30), default='什么都没留下', doc='个性签名')
    avatar = db.Column(db.String(50), default='head.png', doc='用户头像', nullable=False)
    timestamp = db.Column(db.String(25), default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), doc='时间戳', nullable=False)

    friends = db.relationship('Friend', foreign_keys="Friend.one", lazy='dynamic', cascade='all, delete-orphan')

    
    def __repr__(self):
        return '%s <%s>' % (self.nickname, self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_friend(self, friend):
        positive = Friend(one=self.id, other=friend)
        negative = Friend(one=friend, other=self.id)
        db.session.add(positive)
        db.session.add(negative)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'sex': self.sex,
            'city': self.city,
            'signature': self.signature,
            'avatar': '/static/image/' + self.avatar,
            'timestamp': self.timestamp
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'code': 3, 'message': '需要先登录才能进行该操作'})

class Friend(db.Model):
    __tablename__ = "friends"
    one = db.Column(db.String(20), db.ForeignKey(User.id), primary_key=True)
    other = db.Column(db.String(20), db.ForeignKey(User.id), primary_key=True)

# 验证码
class VerifyCode(object):
    def __init__(self, email, code):
        self.email = email
        self.time = time.time()
        self.code = code

    def verify(self, email, code):
        if code == self.code and email == self.email and not self.outOfDate():
            return True
        else:
            return False

    def outOfDate(self):
        return time.time() - self.time > 600