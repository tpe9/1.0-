# coding:utf-8
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
import sys
import json
from django.contrib.auth.hashers import make_password #对密码加密存储
sys.path.append("..")
from account import models, send_email,fun
import random
from datetime import datetime
from django.conf import settings
import base64



def check_token(request):
    find=request.COOKIES.get('id')
    if find:
        user=models.user_token.objects.filter(user=find).count()
        if user:
            user=models.user_token.objects.get(user=find)
            if user.use_token==request.COOKIES.get('user_token'):
                return True
    return False

def show(request):
    user_admin = '退出登录'
    user_url = '/logout/'
    username = request.POST.get('username')
    user = models.Employee.objects.get(username=username)
    pros = models.project.objects.filter(usernum=user.usernum)
    user = []
    num = []
    dateon = []
    dateoff = []
    ord = []
    user2 = []
    num2 = []
    date = []
    ord2 = []
    print('4')

    for pro in pros:
        print('111')
        asks = models.ask_for_perm.objects.filter(pronum=pro.pronum)
        for ask in asks:
            print(ask.order)
            if ask.type == 1:
                bus = models.business.objects.get(order=ask.order)
                print(bus.order)
                user.append(ask.username)
                num.append(bus.usernum)
                dateon.append(bus.dateon.date())
                dateoff.append(bus.dateoff.date())
                ord.append(bus.order)
            else:
                usern = models.Employee.objects.get(username=ask.username)
                leave = models.leave.objects.get(order=ask.order)
                user2.append(ask.username)
                num2.append(usern.usernum)
                date.append(leave.date)
                ord2.append(leave.order)
    print('666')
    context = {'ask': zip(user, num, dateon, dateoff, ord), 'ask2': zip(user2, num2, date, ord2),
               'user_admin': user_admin, 'user_url': user_url}

    return  context




def hello(request):
    return  HttpResponse("hello world!")

def index(request):
    if check_token(request):
        if request.method=="POST":
            if 'accept' in request.POST:
                ord=request.POST.get('order')
                type=request.POST.get('type')
                if int(type)==1:
                    bus=models.business.objects.get(order=int(ord))
                    bus.accept=1
                    bus.save()
                    re=models.ask_for_perm.objects.get(order=bus.order,type=1)
                    re.delete()
                else:
                    leave=models.leave.objects.get(order=int(ord))
                    leave.accept=1
                    leave.save()
                    re = models.ask_for_perm.objects.get(order=leave.order,type=2)
                    re.delete()
            else:
                ord = request.POST.get('order')
                type = request.POST.get('type')
                if int(type) == 1:
                    bus = models.business.objects.get(order=int(ord))
                    re = models.ask_for_perm.objects.get(order=bus.order, type=1)
                    re.delete()
                else:
                    leave = models.leave.objects.get(order=int(ord))
                    re = models.ask_for_perm.objects.get(order=leave.order, type=2)
                    re.delete()
        user_admin='退出登录'
        user_url='/logout/'
        username = request.COOKIES.get('id')
        user = models.Employee.objects.get(username=username)
        pros=models.project.objects.filter(usernum=user.usernum)
        user=[]
        num=[]
        dateon=[]
        dateoff=[]
        ord=[]
        user2=[]
        num2=[]
        date=[]
        ord2=[]
        for pro in pros:
            asks=models.ask_for_perm.objects.filter(pronum=pro.pronum)
            for ask in asks:
                print(ask.order)
                if int(ask.type)==1:
                    bus=models.business.objects.get(order=ask.order)
                    user.append(ask.username)
                    num.append(bus.usernum)
                    dateon.append(bus.dateon.date())
                    dateoff.append(bus.dateoff.date())
                    ord.append(bus.order)
                else:
                    usern = models.Employee.objects.get(username=ask.username)
                    leave = models.leave.objects.get(order=ask.order)
                    user2.append(ask.username)
                    num2.append(usern.usernum)
                    date.append(leave.date)
                    ord2.append(leave.order)
        print('here')
        print(user)

        context = {'ask': zip(user, num, dateon, dateoff, ord), 'ask2': zip(user2, num2, date, ord2),
                   'user_admin': user_admin, 'user_url': user_url}
        return render(request,'mysite/index.html',context)



    else:
        user_admin='登陆'
        user_url='/login/'
    pass
    return render(request,'mysite/index.html',{'user_admin':user_admin,"user_url":user_url})




def logout(request):

    pass
    r=render(request,'mysite/index.html',{'user_admin':'登陆','user_url':'/login'})
    try:
        r.delete_cookie('id')
        r.delete_cookie('user_token')
        return r
    except:
        return r

def login(request):
    message=''
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
    else:
        user_admin = '登陆'
        user_url = '/login/'
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
                        if models.user_token.objects.filter(user=username).count():
                            us_to=models.user_token.objects.get(user=username)
                        else:
                            us_to=models.user_token()
                            us_to.user=username
                            us_to.save()
                        now=datetime.now()
                        token_hash=fun.encrypt_md5(username+str(now).replace(' ',''))
                        us_to.use_token=token_hash
                        us_to.user_last_time=now
                        us_to.save()
                        message='666'
                        print('fi')
                        context=show(request)
                        print('se')
                        r=render(request,'mysite/index.html',context)
                        r.set_cookie('user_token',token_hash,max_age=1000)
                        r.set_cookie('id',username,max_age=600)
                        return r

                    else:
                        message = "密码不正确！"
            except:
                 message = "用户不存在！sad"
        data=json.dumps({"message":message})
        #return HttpResponse(data)
        
        return render(request, 'mysite/login.html',{"message": message})

    return render(request, 'mysite/login.html',locals())



def get_vcode(request):
    message='发送失败'
    if request.method == "POST":
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
                    if delta.days*24*60*60+delta.seconds<60:

                        message='请1分钟稍后发送'
                        return render(request,'mysite/register.html',{"message": message})
                    else:
                        reg.delete()
                try:
                    vericode=random.randint(1000,9999)
                    print(mail)
                    send_email.check_email(mail,vericode)
                    message='发送成功'
                    reg_user = models.Reg_mesg()
                    reg_user.r_email = mail
                    reg_user.r_vcode = str(vericode)
                    reg_user.save()
                except:
                    message='发送邮件失败'

    data=json.dumps({"message":message})
    return HttpResponse(data)





def register(request):
    if request.method == "POST":
        message=''
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
            elif models.Employee.objects.filter(IMEI=IMEI):
                message='同一手机只能登陆一个用户'
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

                            #pic = request.FILES.get('picture')
                            pic=request.POST.get('picture')
                            pic=pic.replace(' ','+')
                            datas = pic.split('base64,')
                            data = base64.b64decode(datas[1])
                            url = settings.MEDIA_ROOT + username + '.jpg'
                            with open(url, 'wb') as f:
                                f.write(data)
                            us_to=models.user_token()
                            us_to.user=username
                            user_profile.save()
                            user.delete()
                            us_to.save()
                            return redirect('/login/')
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
                    print(user.email+f_email)
                    if user.email == f_email:
                        print('1')
                        reg = models.Reg_mesg.objects.filter(r_email=f_email).count()
                        if reg:
                            reg = models.Reg_mesg.objects.get(r_email=f_email)
                            now = datetime.now()
                            d1 = datetime.strptime(str(reg.r_time), '%Y-%m-%d %H:%M:%S.%f')
                            d2 = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f')
                            delta = d2 - d1
                            if delta.days * 24 * 60 * 60 + delta.seconds < 60:

                                message = '请1分钟稍后发送'
                                return render(request, 'mysite/register.html', {"message": message})
                            else:
                                reg.delete()
                        vericode=0
                        try:
                            vericode = random.randint(1000, 9999)
                            send_email.check_email(f_email, vericode)
                            message = '发送成功'
                        except:
                            message = '发送邮件失败'
                        reg_user = models.Reg_mesg()
                        reg_user.r_email = f_email
                        reg_user.r_vcode = str(vericode)
                        reg_user.save()
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
        f_email=request.POST.get('email', None)
        new_passwd = request.POST.get('new_passwd', None)
        new_passwd2 = request.POST.get('new_passwd2', None)
        vcode=request.POST.get('vcode', None)
        if username  and new_passwd:  # 确保用户名和密码都不为空
            
            try:
                user = models.Employee.objects.get(username=username)
                if user:
                    print('1')
                    if new_passwd2 == new_passwd:
                        print(user.password+'2')
                        v=models.Reg_mesg.objects.get(r_email=f_email)
                        print(v)
                        if vcode ==v.r_vcode:
                            user.password =new_passwd
                            print(user.password)
                            user.save()
                            message='修改成功！'
                            return render(request, 'mysite/login.html',{"message": message})
                        else:
                            message='验证码错误'
                    else:
                        message='两次密码不同！'
            except:
                 message = "用户不存在！"
        return render(request, 'mysite/reset_pd.html',{"message": message})
    return render(request, 'mysite/reset_pd.html',{"message": message})



def myinformation_edit(request):
    username=request.COOKIES.get('id')
    user_token=request.COOKIES.get('user_token')
    context={}
    if check_token(request):
        user = models.Employee.objects.get(username=username)
        if request.method=="POST":
            user.email=request.POST.get('email')
            user.age=request.POST.get('age')
            sex_text=request.POST.get('sex')
            if sex_text:user.sex=1
            else:user.sex=0
            user.name=request.POST.get('name')
            user.telenum=request.POST.get('telenum')
            user.position=request.POST.get('position')
            user.home=request.POST.get('homeaddress')
            user.save()
        if user.sex:
            sex_text='男'
        else:
            sex_text='女'
        context={'username':user.username,'email':user.email,'age':user.age,'sex':sex_text,
                 'name':user.name,'telenum':user.telenum,'position':user.position,'homeaddress':user.home,
                 'pronum':user.pronum}

        return render(request, 'mysite/myinformation_edit.html', context)
    else:
        return render(request,'mysite/login.html',{'message':"请先登录"})




def create_pro(request):
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
        username = request.COOKIES.get('id')
        user = models.Employee.objects.get(username=username)
        context={}
        if request.method=="POST":
            num = models.project.objects.filter(usernum=user.usernum).count()
            if num >5:
                return render(request, 'mysite/create_pro.html',{'message':"您创建的项目过多",'pronum':'0','user_url':user_url,'user_admin':user_admin})
            project = models.project()
            while True:
                project.pronum=random.randint(100000,999999)
                if models.project.objects.filter(pronum=project.pronum).count()==0:
                    break
            project.usernum=user.usernum
            project.usernum=user.usernum
            project.location=request.POST.get('location')
            project.company=request.POST.get('company')
            project.timeon=request.POST.get('timeon')
            project.timeoff=request.POST.get('timeoff')
            project.adress=request.POST.get('adress')
            project.save()
            context={'username':user.username,'company':project.company,'location':project.location,
                     'timeon':project.timeon,'timeoff':project.timeoff,'pronum':project.pronum,
                     'message':"创建成功",'user_url':user_url,'user_admin':user_admin}
        else:
            context={'username':user.username,'name':user.name,'user_url':user_url,'user_admin':user_admin}
        return render(request, 'mysite/create_pro.html',context)
    pass
    return render(request, 'mysite/login.html',{'message':'请先登录'})


def project_enter(request):                                                           #加入项目
    context={}
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
        if request.method=="POST":
            username = request.COOKIES.get('id')
            user = models.Employee.objects.get(username=username)
            pronum = request.POST.get('pronum')
            num=models.project.objects.filter(pronum=pronum).count()
            if not num:
                return render(request, "mysite/project_enter.html", {"message": "所选项目不存在",'user_url':user_url,'user_admin':user_admin})
            pro = models.project.objects.get(pronum = pronum)
            if user.pronum!=0 :                                                         #只能加入一个项目
                return render(request,"mysite/project_enter.html",{"message":"您已加入一个项目",'user_url':user_url,'user_admin':user_admin})
            elif pro:                                                               #所选项目不存在
                user.pronum = pronum
                pro=models.project.objects.get(pronum = pronum)
                manage=models.Employee.objects.get(usernum=pro.usernum)
                context={'message':'加入成功','pronum':pronum,'username':manage.username,'name':manage.name,
                         'company':pro.company,'timeon':pro.timeon,'timeoff':pro.timeoff,'location':pro.location,
                         'user_url':user_url,'user_admin':user_admin}
                models.pro_date.objects.create(username=username,
                                               pronum=user.pronum,
                                               dateon=datetime.now().date())
                user.save()
                return render(request, "mysite/project_enter.html", context)
            else:
                return render(request, "mysite/project_enter.html", {"message": "所选项目不存在",'user_url':user_url,'user_admin':user_admin})


        else:
            return render(request,"mysite/project_enter.html")
    return render(request, 'mysite/login.html',{'message':'请先登录'})

def project_inf(request):                                                     #查看项目
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
        if request.method=="POST":
            username = request.COOKIES.get('id')
            user=models.Employee.objects.get(username=username)

            if user.pronum==0:
                return render(request, "mysite/project_inf.html", {"message": "您未参与任何一个项目",'user_url':user_url,'user_admin':user_admin})
            else:
                pro_date = models.pro_date.objects.get(username=username, pronum=user.pronum, dateoff=None)
                pro_date.dateoff = datetime.now().date()
                pro_date.save()
                user.pronum = 0
                user.save()
                return render(request, "mysite/project_inf.html", {"message": "退出项目成功",'user_url':user_url,'user_admin':user_admin})
        else:
            username = request.COOKIES.get('id')
            user = models.Employee.objects.get(username=username)
            if user.pronum==0:                # 未加入项目且未创建项目
                return render(request, "mysite/project_inf.html", {"message": "您未参与任何一个项目",'user_url':user_url,'user_admin':user_admin})
            else:
                if not models.project.objects.filter(pronum=user.pronum):
                    return render(request, "mysite/project_inf.html", {"message": "查询项目无果",'user_url':user_url,'user_admin':user_admin})
                pro1 = models.project.objects.get(pronum=user.pronum)
                user=models.Employee.objects.get(pronum=pro1.pronum,username=username)
                dict = {"pronum": pro1.pronum,
                        "location": pro1.location,
                        "timeon": pro1.timeon,
                        "timeoff": pro1.timeoff,
                        "username":user.username,
                        "usernum": pro1.usernum,
                        "公司": pro1.company,
                        "ps": pro1.notice,'user_url':user_url,'user_admin':user_admin}

            return render(request, "mysite/project_inf.html", dict)
    return render(request, 'mysite/login.html', {'message': '请先登录'})


def check_in(request):
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
        if request.method=="POST":
            username = request.COOKIES.get('id')
            user=models.Employee.objects.get(username=username)
            if user.pronum==0:
                return render(request,'mysite/login.html',{'message':'请先加入项目'})
            pro = models.project.objects.filter(pronum=user.pronum)
            if not pro.count():
                return render(request, 'mysite/login.html', {'message': '项目不存在'})
            pic = request.POST.get('picture')
            location=request.POST.get('geog').split(',')
            pro=models.project.objects.get(pronum=user.pronum)
            location2=pro.location.split(',')
            flag=fun.distance(location[0],location[1],location2[0],location2[1])
            if not flag:
                return render(request, "mysite/check_in.html",
                              {'user_url': user_url, 'user_admin': user_admin, 'message': '打卡位置验证失败'})
            pic = pic.replace(' ', '+')
            datas = pic.split('base64,')
            pic=datas[1]
            flag=fun.face_det(settings.MEDIA_ROOT + username + '.jpg',pic)
            if flag:
                dayset=models.dailycheck()
                dayset.pronum=user.pronum
                dayset.usernum=user.usernum
                dayset.date=datetime.now()
                dayset.timeon=dayset.date.time()
                dayset.timeoff=dayset.date.time()
                print(pro.timeon)
                print(str(dayset.timeon))
                if fun.time_dif(pro.timeon,str(dayset.timeon))<0:
                    dayset.late=0
                dayset.save()
                return render(request, "mysite/index.html", {'message':'验证成功','user_url':user_url,'user_admin':user_admin})
            else:
                return  render(request, "mysite/check_in.html", {'user_url':user_url,'user_admin':user_admin,'message':'人脸验证失败'})
        else:
            return render(request, "mysite/check_in.html", {'user_url':user_url,'user_admin':user_admin})
    return render(request, 'mysite/login.html', {'message': '请先登录'})

def my_project(request):
    if check_token(request):
        user_admin = '退出登录'
        user_url = '/logout/'
        if request.method=="POST":
            if 'delete' in request.POST:
                pronum=request.POST.get('pronum')#删除
                pro=models.project.objects.get(pronum=pronum)
                pro.delete()
                emps=models.project.objects.filter(pronum=pronum)
                for item in emps:
                    item.pronum=0
                    item.save()
                username = request.COOKIES.get('id')#更新前端list
                user = models.Employee.objects.get(username=username)
                list = models.project.objects.filter(usernum=user.usernum)
                number = []
                for item in list:
                    number.append(item.pronum)
                user_list=models.Employee.objects.filter(pronum=pronum)
                for u in user_list:
                    u.pronum=0
                    u.save()
                return render(request,"mysite/my_project.html",{'pro_id':number})
            elif 'save' in request.POST:
                pronum = request.POST.get('pronum')  # 保存
                pro = models.project.objects.get(pronum=pronum)
                pro.location=request.POST.get('location')
                pro.company=request.POST.get('company')
                pro.timeoff=request.POST.get('timeoff')
                pro.timeon=request.POST.get('timeon')
                pro.ps=request.POST.get('ps')
                pro.save()
                pass
            else:
                username = request.COOKIES.get('id')
                user=models.Employee.objects.get(username=username)
                pronum=request.POST.get('pronum')
                print(pronum)
                pro=models.project.objects.get(pronum=pronum)
                context={'pronum':pro.pronum,'username':username,'location':pro.location,'timeon':pro.timeon,
                        'timeoff':pro.timeoff,'ps':pro.ps,'company':pro.company}
                users=models.Employee.objects.filter(pronum=pronum)
                u=[]
                for item in users:
                    u.append(item.username)
                context.update({'users':u})
                return render(request,"mysite/my_project.html",context)
        else:
            username = request.COOKIES.get('id')
            user = models.Employee.objects.get(username=username)
            list=models.project.objects.filter(usernum=user.usernum)
            number=[]
            for item in list:
                number.append(item.pronum)
            return render(request, "mysite/my_project.html", {'pro_id':number})
    return render(request, 'mysite/login.html', {'message': '请先登录'})



def business_apply(request):                                                          #出差申请
    if check_token(request):           #验证
        username = request.COOKIES.get('id')
        user = models.Employee.objects.get(username=username)
        if user.pronum==0:
            return render(request,'mysite/ask_for_leave.html',{'message':'未参加项目，无需出差'})
        busess = models.business.objects.filter(usernum=user.usernum, accept=1)
        searchon = []
        searchoff = []
        day=[]
        timenow=[]
        for item in busess:
            searchon.append(item.dateon)
            searchoff.append(item.dateoff)
            day.append(fun.data_dif(str(item.dateon.date()),str(item.dateoff.date())))
            timenow.append(item.time)
        busess = models.business.objects.filter(usernum=user.usernum, accept=0)
        print(busess)
        searchon2 = []
        searchoff2 = []
        day2 = []
        timenow2=[]
        for item in busess:
            searchon2.append(item.dateon)
            searchoff2.append(item.dateoff)
            day2.append(fun.data_dif(str(item.dateon.date()), str(item.dateoff.date())))
            timenow2.append(item.time)
        context = {'accept': zip(searchon, searchoff,day,timenow),'refuse':zip(searchon2, searchoff2,day2,timenow2)}

        if request.method == 'POST':
            username = request.COOKIES.get('id')
            user = models.Employee.objects.get(username=username)
            dateon=request.POST.get('dateon')
            dateoff = request.POST.get('dateoff')
            s=models.business()
            s.usernum=user.usernum
            s.dateoff=dateoff
            s.dateon=dateon
            s.pronum=user.pronum
            s.save()
            models.ask_for_perm.objects.create(username=username,pronum=user.pronum,type=1,order=s.order)
            context.update({'message':'正在申请，成功后可在列表查询'})
        return render(request,'mysite/business_apply.html',context)
    return render(request,'mysite/login.html',{'message':'请重新登录'})


def check_out(request):
    if check_token(request):
        if request.method=="GET":
            return render(request,'mysite/check_out.html')
        username = request.COOKIES.get('id')
        user = models.Employee.objects.get(username=username)
        pro=models.project.objects.get(pronum=user.pronum)
        now=datetime.now()
        dayset=models.dailycheck.objects.filter(usernum=user.usernum,pronum=user.pronum)
        if not dayset.count():
            return  render(request, 'mysite/index.html', {'message': '您未上班打卡'})
        dayset = models.dailycheck.objects.get(usernum=user.usernum, pronum=user.pronum)
        flag=1
        if fun.time_dif(pro.timeoff,str(now.time()))>0:
            dayset.leave=0
            dayset.timeoff=datetime.now().time()
            dayset.save()
            flag=0
        return render(request, 'mysite/index.html', {'flag': flag})




        pass
    return render(request, 'mysite/login.html', {'message': '请重新登录'})

def ask_for_leave(request):
    if check_token(request):
        username = request.COOKIES.get('id')
        user = models.Employee.objects.get(username=username)
        if user.pronum==0:
            return render(request,'mysite/ask_for_leave.html',{'message':'未参加项目，无需请假'})
        leaves=models.leave.objects.filter(usernum=user.usernum,accept=1)
        date=[]
        pron=[]
        timenow=[]
        for item in leaves:
            date.append(item.date)
            pron.append(item.pronum)
            timenow.append(item.time)
        print(date)
        leaves = models.leave.objects.filter(usernum=user.usernum, accept=0)
        date2 = []
        pron2 = []
        timenow2=[]
        for item in leaves:
            date2.append(item.date)
            pron2.append(item.pronum)
            timenow2.append(item.time)
        print(pron2)
        context={'accept':zip(date,pron,timenow),'refuse':zip(date2,pron2,timenow2)}
        if request.method=="POST":
            date=request.POST.get('date')
            s=models.leave()
            s.pronum=user.pronum
            s.usernum=user.usernum
            s.date=date
            s.save()
            context.update({'message':'请假已提交，成功后会在记录中显示'})
            models.ask_for_perm.objects.create(username=username, pronum=user.pronum, type=2, order=s.order)
            pass
        return render(request,'mysite/ask_for_leave.html',context)




    return render(request, 'mysite/login.html', {'message': '请重新登录'})