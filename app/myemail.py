#coding: utf-8  
import smtplib, ConfigParser  
from email.mime.text import MIMEText  
from email.header import Header  
 

subject = '微聊验证码'  
smtpserver = 'smtp.qq.com'  

cp = ConfigParser.SafeConfigParser()
cp.read('server.conf')
username = cp.get('email', 'username') 
password = cp.get('email', 'password')
  
def send(email, message):
	receiver = [] 
	receiver.append(email)
	msg = MIMEText(message, 'plain', 'utf-8')#中文需参数‘utf-8’，单字节字符不需要  
	msg['Subject'] = Header(subject, 'utf-8')  
	msg['From'] = "MiniChat<926367174@qq.com>"
	try:
	    smtp = smtplib.SMTP()
	    smtp.connect(smtpserver) 
	    smtp.starttls()
	    smtp.login(username, password)  
	    smtp.sendmail(username, receiver, msg.as_string())  
	    smtp.quit()  
	    return True
	except Exception, e:  
		print u'发送失败'
		print str(e)
		return False
	    
if __name__ == '__main__':
	message = "test"  
	send(message)