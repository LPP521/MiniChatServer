# coding=utf-8
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf8')
import json, re, random, xinge_push
import thread
import time

from flask import Blueprint, request, jsonify, current_app
from models import db, User, Friend, VerifyCode
from flask_login import login_required
from flask_login import login_user, logout_user, current_user
import myemail, datetime

main = Blueprint('main', __name__)
verify_Code = {}
LoginUser = []
unsendMessage = []
admin = "1234"

# 读取配置信息
cp = ConfigParser.SafeConfigParser()
cp.read('server.conf')
accessId = cp.get('xinge', 'accessId')
secretKey = cp.get('xinge', 'secretKey')
#create XingeApp
# 第一个参数是 accessId， 第二个是 secretKey
xinge = xinge_push.XingeApp(accessId, secretKey)

def buildMessage(title, type, sender, message):
    msg = xinge_push.Message()
    msg.type = xinge_push.MESSAGE_TYPE_ANDROID_NOTIFICATION
    msg.title = title
    msg.style = xinge_push.Style(0, 1, 1, 1, nId=1)
    msg.custom = {"type": type, "sender": sender, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    msg.content = message
    return msg

def sendMessage(receiver, title, type, sender, message):
    msg = buildMessage(title, type, sender, message)
    user = User.query.filter_by(id=receiver).first()
    if user.id in LoginUser:
        code, msg = xinge.PushSingleAccount(0, receiver, msg)
        if code:
            unsendMessage.append({'receiver': receiver, "message": msg})
    else:
        unsendMessage.append({'receiver': receiver, "message": msg})

def resendMessage():
    while True:
        time.sleep(5)
        for msg in unsendMessage:
            user = User.query.filter_by(id=msg['receiver']).first()
            # print 'trying to resend message to', msg['receiver'], "..."
            if user and (user.id in LoginUser):
                code, msg = xinge.PushSingleAccount(0, msg['receiver'], msg)
                if not code:
                    unsendMessage.remove(msg)

try:
    thread.start_new_thread(resendMessage, ())
except Exception, e:
    print str(e)
    print "Error: unable to start thread"

@main.route('/register', methods=['POST'])
def regesiter():
    email = request.form['id']
    findUser = User.query.filter_by(id=email).first()
    if findUser:
        return jsonify({'code': 1, 'message': '邮箱已被注册'})

    code = request.form['code']
    isCodeValid = False
    for id in verify_Code.keys():
        if verify_Code[id].outOfDate():
            verify_Code.pop(id)
            continue
        if id == email and verify_Code[id].verify(code):
            isCodeValid = True

    if not isCodeValid:
        return jsonify({'code': 1, 'message': '验证码已失效'})
    
    user = User()
    user.id = request.form['id']
    user.nickname = request.form['nickname']
    user.password = request.form['password']
    user.timestamp = request.form.get('timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        LoginUser.append(user.id)
        return jsonify({'code': 0, 'message': current_user.to_json()})
    elif user:
        return jsonify({'code': 2, 'message': '密码错误'})
    else:
        return jsonify({'code': 2, 'message': '账号不存在'})

@main.route('/logout')
@login_required
def logout():
    if current_user.id in LoginUser:
        LoginUser.remove(current_user.id)
    logout_user()
    return jsonify({'code': 0, 'message': '登出成功'})

@main.route('/verifyOldPassword', methods=['POST'])
@login_required
def verifyOldPassword():
    old_password = request.form['password']
    if current_user.verify_password(old_password):
        return jsonify({'code': 0, 'message': '密码正确'})
    else:
        return jsonify({'code': 2, 'message': '密码错误'})


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
    
    timestamp = form.get('timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    current_user.timestamp = timestamp

    db.session.add(current_user)
    db.session.commit()
    return jsonify({'code': 0, 'message': '修改成功'})

@main.route('/resetPassword', methods=['POST'])
def resetPassword():
    id = request.form['id']
    password = request.form['password']
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'code': 2, 'message': '账号不存在'})
    user.password = password
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 0, 'message': '密码重置成功'})


@main.route('/getUserInfo', methods=['GET'])
@login_required
def getUserInfo():
    return jsonify({'code': 0, 'message': current_user.to_json()})

@main.route('/getTimestamp/<id>')
def getTimestamp(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({'code': 0, 'message': user.timestamp})
    else:
        return jsonify({'code': 2, 'message': '账号不存在'})

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
    message = "[微聊]您的验证码是%s, 10分钟内有效。为了您的信息安全，请勿泄露验证码" %str(code)
    if myemail.send(id, message):
        verify_Code[id] = VerifyCode(str(code))
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
    for id in verify_Code.keys():
        if verify_Code[id].outOfDate():
            verify_Code.pop(id)
            continue
        if id == email and verify_Code[id].verify(code):
            isCodeValid = True

    if not isCodeValid:
        return jsonify({'code': 11, 'message': '验证码不正确'})
    return jsonify({'code': 0, 'message': '验证码正确'})

@main.route('/friend/addRequest', methods=['POST'])
@login_required
def addRequest():
    friend = request.form['friend']

    if friend == current_user.id:
        return jsonify({'code': 7, 'message': '不能和自己成为好友'})
    if current_user.friends.filter_by(other=friend).first():
        return jsonify({'code': 8, 'message': '不能重复添加好友'})

    findUser = User.query.filter_by(id=friend).first()
    if findUser:
        sendMessage(friend, "好友申请", 1, current_user.id, current_user.nickname + "请求添加您为好友")
        return jsonify({'code': 0, 'message': '已发送好友请求，等候对方同意'})
    else:
        return jsonify({'code': 10, 'message': '添加的好友不存在'})


@main.route('/friend/answer', methods=['POST'])
@login_required
def addFriend():
    friend = request.form['friend']
    answer = request.form['answer']
    if answer == "no":
        sendMessage(friend, "拒绝申请", 0, admin, current_user.nickname + "拒绝了您的好友请求")
        return jsonify({'code': 0, 'message': '发送成功'})
    if friend == current_user.id:
        return jsonify({'code': 7, 'message': '不能和自己成为好友'})
    if current_user.friends.filter_by(other=friend).first():
        return jsonify({'code': 8, 'message': '不能重复添加好友'})
    user = User.query.filter_by(id=friend).first()   
    if user:
        current_user.add_friend(friend)
        sendMessage(friend, "好友申请", 0, current_user.id, "我同意了您的好友请求，我们可以开始聊天了")
        return jsonify({'code': 0, 'message': '成功添加好友'})
    else:
        return jsonify({'code': 9, 'message': '添加的好友不存在'})

@main.route('/getFriends')
@login_required
def getFrineds():
    # 返回每个好友的详细信息
    # friends = User.query.filter(User.id.in_([f.other for f in current_user.friends])).all()
    # return jsonify({'code': 0, 'message': [f.to_json() for f in friends]})

    # 返回好友 id List
    return jsonify({'code': 0, 'message': [f.other for f in current_user.friends]})

@main.route('/isFriend', methods=["POST"])
@login_required
def isFriend():
    friend = request.form['friend']
    user = User.query.filter_by(id=friend).first()
    if not user:
        return jsonify({'code': 4, 'message': '该用户不存在'})
    if current_user.friends.filter_by(other=friend).first():
        return jsonify({'code': 0, 'message': 'yes'})
    else:
        return jsonify({'code': 0, 'message': 'no'})


@main.route('/send', methods=["POST"])
@login_required
def send():
    receiver = request.form['receiver']
    message = request.form['message']
    friend = current_user.friends.filter_by(other=receiver).first()
    if not friend:
        return jsonify({'code': 13, 'message': '非好友不能发送消息'})  
    sendMessage(receiver, "微聊消息", 0, current_user.id, message)
    return jsonify({'code': 0, 'message': '消息发送成功'})    

@main.route('/friend/delete', methods=["POST"])
@login_required
def deleteFriend():
    friend = request.form['friend']
    user = User.query.filter_by(id=friend).first()
    f = current_user.friends.filter_by(other=friend).first()
    if f:
        db.session.delete(f)
        f_inverse = user.friends.filter_by(other=current_user.id).first()
        db.session.delete(f_inverse)
        return jsonify({'code': 0, 'message': '删除成功'})
    else:
        return jsonify({'code': 13, 'message': '非好友关系不能删除'})    