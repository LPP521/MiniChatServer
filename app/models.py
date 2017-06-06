# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.String(11), doc='手机号码', primary_key=True)
    nickname = db.Column(db.String(20), doc='昵称', default='微聊用户', nullable=False)
    password_hash = db.Column(db.String(128), doc='密码散列值', nullable=False)
    
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

    def __json__(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
        }