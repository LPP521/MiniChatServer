# coding=utf-8
import json, re, random
from flask import Blueprint, request, jsonify, current_app
from models import db, User, Friend, verifyCode
from flask_login import login_required
from flask_login import login_user, logout_user, current_user
import myemail

main = Blueprint('main', __name__)
verify_Code = []

@main.route('/register', methods=['POST'])
def regesiter():
    email = request.form['id']
    findUser = User.query.filter_by(id=email).first()
    if findUser:
        return jsonify({'code': 1, 'message': '邮箱已被注册'})

    code = request.form['code']
    isCodeValid = False
    for c in verify_Code:
        if c.verify(email, code):
            isCodeValid = True
        elif c.outOfDate():
            verify_Code.remove(c)
    if not isCodeValid:
        return jsonify({'code': 1, 'message': '验证码已失效'})
    
    user = User()
    user.id = request.form['id']
    user.nickname = request.form['nickname']
    user.password = request.form['password']
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 0, 'message': '注册成功'})

@main.route('/login', methods=['POST'])
def login():
    id = request.form['id']
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

@main.route('/getVerifycode/<id>')
def sendVerifycode(id):
    if not re.match("[a-zA-Z0-9]+\@+[a-zA-Z0-9]+\.+[a-zA-Z]", id) != None:
        return jsonify({'code': 5, 'message': '邮箱格式非法'})
    code = random.randint(1000, 9999)
    verify_Code.append(verifyCode(id, str(code)))
    message = "[微聊]您的验证码是%s, 10分钟内有效。为了您的信息安全，请勿泄露验证码" %str(code)
    if myemail.send(id, message):
        return jsonify({'code': 0, 'message': '验证码发送成功'})
    else:
        return jsonify({'code': 6, 'message': '发送失败，请稍后再试'})

@main.route('/verifyCode', methods=['POST'])
def verifyCode():
    email = request.form['id']
    findUser = User.query.filter_by(id=email).first()
    if not findUser:
        return jsonify({'code': 10, 'message': '该邮箱尚未注册'})

    code = request.form['code']
    isCodeValid = False
    for c in verify_Code:
        if c.verify(email, code):
            isCodeValid = True
        elif c.outOfDate():
            verify_Code.remove(c)
    if not isCodeValid:
        return jsonify({'code': 11, 'message': '验证码不正确'})
    return jsonify({'code': 0, 'message': '验证码正确'})

@main.route('/addFriend', methods=['POST'])
@login_required
def queryTest():
    friend = request.form['friend']
    if friend == current_user.id:
        return jsonify({'code': 7, 'message': '不能和自己成为好友'})
    if Friend.query.filter_by(one=friend).first():
        return jsonify({'code': 8, 'message': '不能重复添加好友'})
    user = User.query.filter_by(id=friend).first()   
    if user:
        current_user.add_friend(friend)
        return jsonify({'code': 0, 'message': '成功添加好友'})
    else:
        return jsonify({'code': 9, 'message': '添加的好友不存在'})

@main.route('/getFrineds')
@login_required
def getFrineds():
    friends = User.query.filter(User.id.in_([f.other for f in current_user.friends])).all()
    return jsonify({'code': 0, 'message': [f.to_json() for f in friends]})