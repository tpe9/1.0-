from django.db import models



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
	IMEI = models.CharField(max_length=16,unique=True)
	telenum = models.IntegerField(max_length=15,null=True)
	password = models.CharField(max_length=100)
	email = models.EmailField(max_length=20,unique=True)
	sex = models.BooleanField(max_length=1,choices=((0,'男'),(1,'女')),null=True)
	position = models.CharField(max_length=10,null=True)
	name =  models.CharField(max_length=20,null=True)
	pronum = models.IntegerField(max_length=10,null=True,default=0)
	home = models.CharField(max_length=100,null=True,verbose_name = '家庭住址')
	age = models.IntegerField(max_length=2,null=True,verbose_name = '年龄')
	department=models.CharField(max_length=100,null=True)
	birthday = models.DateField(max_length=20,null=True)


	def __str__(self):
		return str(self.usernum)

	class Meta:
		ordering = ['usernum']
		verbose_name = '员工'
		verbose_name_plural= '员工'

class project(models.Model):
	pronum = models.IntegerField(max_length=20, unique=True)
	usernum = models.IntegerField(max_length=10)
	location = models.CharField(max_length=35)
	date=models.DateTimeField(auto_now=True)
	adress =  models.CharField(max_length=100,null=True)
	timeon = models.CharField(max_length=10)
	timeoff = models.CharField(max_length=10)
	ps = models.CharField(max_length=100,null=True)
	company = models.CharField(max_length=20, verbose_name = '公司名',null=True)
	notice=models.CharField(max_length=200,null=True)


	def __str__(self):
		return str(self.pronum)

	class Meta:
		ordering = ['pronum']
		verbose_name = '项目'
		verbose_name_plural= '项目'

class dailycheck(models.Model):
	usernum = models.IntegerField(max_length=6)
	pronum = models.IntegerField(max_length=6)
	date = models.DateTimeField(max_length=20)
	timeon = models.TimeField(max_length=10)
	timeoff = models.TimeField(max_length=10)
	late=models.BooleanField(default=1)
	leave=models.BooleanField(default=1)


	def __str__(self):
		return str(self.usernum)

	class Meta:
		ordering = ['usernum']
		verbose_name = '上班记录'
		verbose_name_plural= '上班记录'


class leave(models.Model):
	order= models.AutoField(primary_key=True)
	pronum = models.IntegerField(max_length=6)
	usernum = models.IntegerField(max_length=6)
	date = models.CharField(max_length=10,verbose_name = '请假日期时间')
	accept=models.BooleanField(default=0)
	time = models.DateTimeField(auto_now=True)
	def __str__(self):
		return str(self.usernum)

	class Meta:
		ordering = ['usernum']
		verbose_name = '请假记录'
		verbose_name_plural= '请假记录'



class business(models.Model):
	order=models.AutoField(primary_key=True)
	usernum = models.IntegerField(max_length=6)
	pronum = models.IntegerField(max_length=6)
	dateon = models.DateTimeField(max_length=10)
	dateoff = models.DateTimeField(max_length=10)
	accept =models.BooleanField(default=0)
	time=models.DateTimeField(auto_now=True)


	def __str__(self):
		return str(self.usernum)

	class Meta:
		ordering = ['usernum']
		verbose_name = '出差记录'
		verbose_name_plural= '出差记录'









class user_token(models.Model):
	user=models.CharField(max_length=8)
	use_token=models.CharField(max_length=100,null=True)
	user_last_time=models.DateTimeField(max_length=20,null=True)



class dayoff(models.Model):
	pronum = models.IntegerField(max_length=10, null=True, default=0)
	date = models.CharField(max_length=10, verbose_name='休息日期')
	class Meta:
		verbose_name = '休息日'
		verbose_name_plural='休息日'



class dayon(models.Model):
	pronum = models.IntegerField(max_length=10, null=True, default=0)
	date = models.CharField(max_length=10, verbose_name='休息日期')



	class Meta:
		verbose_name = '加班'
		verbose_name_plural='加班'


class ask_for_perm(models.Model):
	username=models.CharField(max_length=30)
	pronum = models.IntegerField(max_length=10, null=True, default=0)
	type = models.IntegerField(max_length=1)
	order=models.IntegerField(max_length=10)



	class Meta:
		verbose_name = '请求'
		verbose_name_plural='请求'




class pro_date(models.Model):
	username=models.CharField(max_length=30)
	pronum = models.IntegerField(max_length=10)
	dateon = models.DateField(max_length=10)
	dateoff = models.DateField(null=True)


	class Meta:
		verbose_name = '历史项目'
		verbose_name_plural='历史项目'