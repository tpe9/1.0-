# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render,redirect
import sys
from django.contrib.auth.hashers import make_password #对密码加密存储
sys.path.append("..")
from account import models, send_email
import random
from datetime import datetime

def hello(request):
	return  HttpResponse("hello world!")

def index(request):
    pass
    return render(request,'mysite/index.html')




def logout(request):
    pass
    return render(request,'/index/')

def login(request):
    if request.method == "POST":
        if 'forget' in request.POST:
            return render(request, 'mysite/forget.html')
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.Employee.objects.get(username=username)
                if user:
                    if user.password == password:
                        return redirect('/index/')
                    else:
                        message = "密码不正确！"
            except:
                 message = "用户不存在！"
        return render(request, 'mysite/login.html',{"message": message})
    return render(request, 'mysite/login.html',locals())







def register(request):
    if request.method == "POST":
        message=''
        if 'code_but' in request.POST:
            username = request.POST.get('username', None)
            mail = request.POST.get('email', None)
            if username and mail:
                if models.Employee.objects.filter(username=username).count():
                   message='该名已存在'
                elif models.Employee.objects.filter(email=mail).count():
                    message='该邮箱已注册'
                else:
                    reg = models.Reg_mesg.objects.filter(r_email=mail)
                    if reg.count():
                        reg=models.Reg_mesg.objects.get(r_email=mail)
                        now = datetime.now()
                        d1 = datetime.strptime(str(reg.r_time), '%Y-%m-%d %H:%M:%S.%f')
                        d2 = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
                        delta=d2-d1
                        print('666666')
                        if delta.days*24*60*60+delta.seconds<60:
                            print(delta.days*24*60*60+delta.seconds)

                            message='请1分钟稍后发送'
                            return render(request,'mysite/register.html',{"message": message})
                        else:
                        	reg.delete()
                    try:
                        vericode=random.randint(1000,9999)
                        print(mail)
                        send_email.check_email(mail,vericode)
                        print('send')
                    except:
                        message='发送邮件失败'
                    reg_user = models.Reg_mesg()
                    reg_user.r_email=mail
                    reg_user.r_vcode=str(vericode)
                    reg_user.save()
        else:
            username = request.POST.get('username', None)
            mail = request.POST.get('email', None)
            password = request.POST.get('password', None)
            vcode = request.POST.get('vcode',None)
            IMEI = request.POST.get('IMEI',None)
            if username and password and mail and IMEI:  # 确保用户名和密码都不为空
                username = username.strip()
                # 用户名字符合法性验证
                # 密码长度验证
                # 更多的其它验证.....
                if models.Employee.objects.filter(username=username).count():
                    message='用户名已存在.'
                elif models.Employee.objects.filter(email=mail).count():
                    message='该邮箱已注册'
                else:

                    user = models.Reg_mesg.objects.filter(r_email=mail)
                    if user.count():
                        user = models.Reg_mesg.objects.get(r_email=mail)
                        reg = models.Reg_mesg.objects.get(r_email=mail)
                        now = datetime.now()
                        d1 = datetime.strptime(str(reg.r_time), '%Y-%m-%d %H:%M:%S.%f')
                        d2 = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
                        delta=d2-d1
                        print('2')
                        if reg and delta.days*24*60*60+delta.seconds<3600 :
                            print('1')
                            if vcode == user.r_vcode:
                                user_profile = models.Employee()
                                user_profile.username = username
                                user_profile.email = mail
                                user_profile.IMEI=IMEI
                                user_profile.password = password #make_password(password)
                                user_profile.save()
                                user.delete()
                                return redirect('/index/')
                            else:
                                message='验证码错误'
                        else:
                            message='验证码超时'
                    else:
                    	message='验证码错误'
            else:
                message='信息不完整'
                    	
        return render(request,'mysite/register.html',{"message": message})         
    return render(request,'mysite/register.html',locals())



def forget(request):
    message=''
    if request.method == "POST":
        username = request.POST.get('username', None)
        f_email = request.POST.get('mail', None)
        if username and f_email:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.Employee.objects.get(username=username)
                if user:
                    if user.u_email == f_email:
                        return render(request, 'mysite/reset_pd.html')
                    else:
                        message = "邮箱不正确！"
            except:
                 message = "用户不存在！"
        return render(request, 'mysite/forget.html',{"message": message})
    return render(request, 'mysite/forget.html',{"message": message})











def reset_pd(request):
    message=''
    if request.method == "POST":
        username = request.POST.get('username', None)
        old_passwd = request.POST.get('old_passwd', None)
        new_passwd = request.POST.get('new_passwd', None)
        new_passwd2 = request.POST.get('new_passwd2', None)
        if username and old_passwd and new_passwd:  # 确保用户名和密码都不为空
            
            try:
                user = models.Employee.objects.get(username=username)
                if user:
                    if new_passwd2 == new_passwd:
                        print('111')
                        if user.passwd==old_passwd:
                            user.passwd =new_passwd
                            print(user.passwd)
                            user.save()
                            message='修改成功！'
                            return render(request, 'mysite/login.html',{"message": message})
                        else:
                            message='密码错误！'
                    else:
                        message='两次密码不同！'
            except:
                 message = "用户不存在！"
        return render(request, 'mysite/reset_pd.html',{"message": message})
    return render(request, 'mysite/reset_pd.html',{"message": message})







