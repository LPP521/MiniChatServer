from flask import Blueprint
from models import db, User


main = Blueprint('main', __name__)

@main.route('/regesiter/<id>/<username>')
def regesiter(id, username):
    user = User(id=id, nickname=username)
    db.session.add(user)
    db.session.commit()
    return 'User %s' % username

@main.route('/login/<id>')
def login(id):
    user = User.query.filter_by(id=id).first()
    return 'User %s' % user.nickname