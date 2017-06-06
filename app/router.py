from flask import Blueprint
from models import db, User


main = Blueprint('main', __name__)

@main.route('/regesiter/<id>/<username>/<password>')
def regesiter(id, username, password):
    user = User(id=id, nickname=username, password=password)
    db.session.add(user)
    db.session.commit()
    return 'User %s' % username

@main.route('/login/<id>/<password>')
def login(id, password):
    user = User.query.filter_by(id=id).first()
    if user.verify_password(password):
        return 'User %s' % user.nickname
    else:
        return 'wrong password'