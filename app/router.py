# coding=utf-8
import json
from flask import Blueprint, request, jsonify
from models import db, User
from flask_login import login_required
from flask_login import login_user, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def regesiter():
    findUser = User.query.filter_by(id=request.form['phone']).first()
    if findUser:
        return '手机号已被注册'
    user = User()
    user.id = request.form['phone']
    user.nickname = request.form['nickname']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()
    return u'注册成功， User %s' % user.nickname

@main.route('/login/<id>/<password>')
def login(id, password):
    user = User.query.filter_by(id=id).first()
    if user.verify_password(password):
        login_user(user)
        return jsonify(user.to_json())
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

@main.route('/updateUser/<id>', methods=['GET', 'POST'])
@login_required
def updateUser(id):
    user = User.query.filter_by(id=id).first()
    if user and current_user == user:
        user.nickname = request.form['nickname']
        user.password = request.form['password']
        user.mini_number = request.form['mini_number']
        user.sex = request.form['sex']
        user.city = request.form['city']
        user.signature = request.form['signature']
        db.session.add(user)
        db.session.commit()
        return u'更新成功， User %s' % user.nickname
    else:   
        return u'用户不存在'
