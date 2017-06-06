from flask import Blueprint
from models import db, User
from flask_login import login_required
from flask_login import login_user, logout_user

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
        login_user(user)
        return 'User %s' % user.nickname
    else:
        return 'wrong password'

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You have been logged out.'

@main.route('/secret/<id>')
@login_required
def secret(id):
    user = User.query.filter_by(id=id).first()
    return 'User %s' % user.nickname