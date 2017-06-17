# coding=utf-8
import json
from flask import Blueprint, request, jsonify, current_app
from models import db, User
from flask_login import login_required
from flask_login import login_user, logout_user, current_user

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def regesiter():
    findUser = User.query.filter_by(id=request.form['phone']).first()
    if findUser:
        return jsonify({'code': 1, 'message': '邮箱已被注册'})
    user = User()
    user.id = request.form['phone']
    user.nickname = request.form['nickname']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 0, 'message': '注册成功'})

@main.route('/login', methods=['POST'])
def login():
    id = request.form['phone']
    password = request.form['password']
    user = User.query.filter_by(id=id).first()
    if user and user.verify_password(password):
        login_user(user)
        return jsonify({'code': 0, 'message': '登录成功'})
    elif user:
        return jsonify({'code': 2, 'message': '密码错误'})
    else:
        return jsonify({'code': 2, 'message': '账号不存在'})

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'code': 0, 'message': '登出成功'})


@main.route('/updateUser', methods=['POST'])
@login_required
def updateUser():
    form = request.form
    nickname = form.get('nickname', '').strip()
    if nickname != '':
        current_user.nickname = nickname

    password = form.get('password', '').strip()
    if password != '':
        current_user.password = password

    sex = form.get('sex', '').strip()
    if sex != '':
        current_user.sex = sex        

    city = form.get('city', '').strip()
    if city != '':
        current_user.city = city      

    signature = form.get('signature', '').strip()
    if signature != '':
        current_user.signature = signature      

    avatar = request.files.get('avatar', None)
    if avatar:
        filename = avatar.filename
        filename = "%s%s" % (current_user.id, filename[filename.rindex('.'):])
        url = '%s/image/%s' % (current_app.static_folder, filename)
        current_user.avatar = filename
        avatar.save(url)

    db.session.add(current_user)
    db.session.commit()
    return jsonify({'code': 0, 'message': '修改成功'})

@main.route('/getUserInfo', methods=['GET'])
@login_required
def getUserInfo():
    return jsonify({'code': 0, 'message': current_user.to_json()})

@main.route('/query/<id>')
def queryById(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({'code': 0, 'message': user.to_json()})
    else:
        return jsonify({'code': 4, 'message': '该用户不存在'})
