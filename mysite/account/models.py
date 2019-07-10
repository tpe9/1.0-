from django.db import models

# Create your models here.
class Users(models.Model):
    user_ID = models.CharField(max_length=30, unique=True)
    u_email = models.CharField(max_length=30, unique=True)
    passwd = models.CharField(max_length=16)
    UUID = models.CharField(max_length=16)



    def __str__(self):
        return self.user_ID

    class Meta:
        ordering = ['user_ID']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Reg_mesg(models.Model):
    r_email = models.CharField(max_length=30, unique=True)
    r_vcode = models.CharField(max_length=5)
    r_time = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.r_email

    class Meta:
        ordering = ['r_email']
        verbose_name = '注册'
        verbose_name_plural = '注册'




class Employee(models.Model):
	usernum = models.AutoField(primary_key=True)
	username=models.CharField(max_length=30)
	IMEI = models.IntegerField(max_length=16,unique=True)
	telenum = models.IntegerField(max_length=15,null=True)
	password = models.CharField(max_length=100)
	email = models.EmailField(max_length=20,unique=True)
	photo = models.ImageField(upload_to='img',null=True)
	sex = models.BooleanField(max_length=1,choices=((0,'男'),(1,'女')),null=True)
	position = models.CharField(max_length=10,null=True)
	name =  models.CharField(max_length=20,null=True)
	pronum = models.IntegerField(max_length=10,null=True)


	def __str__(self):
		return str(self.usernum)

	class Meta:
		ordering = ['usernum']
		verbose_name = '员工'
		verbose_name_plural= '员工'

class project(models.Model):
	pronum = models.IntegerField(max_length=20, unique=True)
	usernum = models.IntegerField(max_length=10)
	location = models.CharField(max_length=20)
	timeon = models.CharField(max_length=10)
	timeoff = models.CharField(max_length=10)
	ps = models.CharField(max_length=100,blank=True)#备注


	def __str__(self):
		 return self.pronumclass

	class Meta:
		ordering = ['pronum']
		verbose_name = '项目'
		verbose_name_plural= '项目'

class dailycheck(models.Model):
	usernum = models.IntegerField(max_length=6)
	date = models.DateTimeField(max_length=10)
	timeon = models.CharField(max_length=10)
	timeoff = models.CharField(max_length=10)
	leave = models.BooleanField(max_length=1, choices=((0, '否'), (1, '是')))#请假

	def __str__(self):
		return self.usernum

	class Meta:
		ordering = ['usernum']
		verbose_name = '上班记录'
		verbose_name_plural= '上班记录'


class leave(models.Model):
	usernum = models.IntegerField(max_length=6)
	date = models.DateTimeField(max_length=10)
	timeon = models.CharField(max_length=10)
	timeoff = models.CharField(max_length=10)
	def __str__(self):
		return self.usernum

	class Meta:
		ordering = ['usernum']
		verbose_name = '请假记录'
		verbose_name_plural= '请假记录'



class out_buss(models.Model):
	usernum = models.IntegerField(max_length=6)
	dateon = models.DateTimeField(max_length=10)
	dateoff = models.DateTimeField(max_length=10)


	def __str__(self):
		return self.usernum

	class Meta:
		ordering = ['usernum']
		verbose_name = '出差记录'
		verbose_name_plural= '出差记录'




class extra(models.Model):
	usernum = models.IntegerField(max_length=6)
	date = models.DateTimeField(max_length=10)
	timeoff = models.CharField(max_length=10)

	def __str__(self):
		return self.usernum


	class Meta:
		ordering = ['usernum']
		verbose_name = '加班记录'
		verbose_name_plural= '加班记录'





















    