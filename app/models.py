# coding=utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户"""
    __tablename__ = 'users'

    id = db.Column(db.String(11), doc='手机号码', primary_key=True)
    nickname = db.Column(db.String(20), doc='昵称', default='微聊用户', nullable=False)

    def __repr__(self):
        return '%s <%s>' % (self.nickname, self.id)

    def __json__(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
        }