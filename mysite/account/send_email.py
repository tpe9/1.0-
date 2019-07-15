#!/usr/bin/python3
 
import smtplib
import email.mime.multipart
import email.mime.text



def check_email(msgTo, vericode):
	msg = email.mime.multipart.MIMEMultipart()
	msgFrom = '1639938697@qq.com' #从该邮箱发送
	#msgTo = '308121169@qq.com' #发送到该邮箱
	smtpSever='smtp.qq.com' # 163邮箱的smtp Sever地址
	smtpPort = '25' #开放的端口
	sqm='sawfzffqmcacdgfi' # 在登录smtp时需要login中的密码应当使用授权码而非账户密码
	 
	msg['from'] = 'shybee'+'<'+msgFrom+'>'
	msg['to'] = 'njh'+'<'+msgTo+'>'
	msg['subject'] = 'shybee'
	content = '''
	你好:
	  这是一封CI考勤验证邮件,您的验证码为
	'''+str(vericode)+'，如果不是本人操作，请忽略。'
	txt = email.mime.text.MIMEText(content)
	msg.attach(txt)
	smtp = smtplib
	smtp = smtplib.SMTP()
	'''
	smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
	'''
	smtp.connect(smtpSever, smtpPort)
	smtp.login(msgFrom, sqm)
	smtp.sendmail(msgFrom, msgTo, str(msg))
	# s = smtplib.SMTP("localhost")
	# s.send_message(msg)
	smtp.quit()