# coding=utf-8

import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf8')

import json
import xinge_push

from flask import Flask
from flask import request
app = Flask(__name__)

# 读取配置信息
cp = ConfigParser.SafeConfigParser()
cp.read('server.conf')
accessId = cp.get('xinge', 'accessId')
secretKey = cp.get('xinge', 'secretKey')
#create XingeApp
# 第一个参数是 accessId， 第二个是 secretKey
xinge = xinge_push.XingeApp(accessId, secretKey)

#build your message
msg = xinge_push.Message()
msg.type = xinge_push.MESSAGE_TYPE_ANDROID_NOTIFICATION
msg.title = '微聊消息'
msg.content = ''

# src是发送人，des是接收人，msg是发送的消息
@app.route('/<src>/<des>', methods=['GET', 'POST'])
def send(src, des):
    msg.content = request.args.get('msg', 'defaultMsg')
    print "src： ", src
    print "des： ", des

    # 发送给单个账号
    ret_code, error_msg = xinge.PushSingleAccount(0, des, msg)
    # 返回码为0表示发送成功，否则失败
    if ret_code:
        print "push failed! retcode:", ret_code, "error_msg:", error_msg
    else:
        print "push successfully!"
    return msg.content

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


if __name__ == '__main__':
    app.debug=True
    # 使得服务器对外部开放
    app.run(host='0.0.0.0')
