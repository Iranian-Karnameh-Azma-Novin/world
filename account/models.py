from django.db import models
from django.contrib.auth.models import User , AbstractBaseUser ,PermissionsMixin
from .managers import UserManager
# Create your models here.




class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length= 100,unique=True,verbose_name='email')
	phone_number = models.CharField(max_length= 10,unique=True)
	is_active = models.BooleanField(default= True)
	is_admin =  models.BooleanField(default= True)
	name = models.CharField(max_length= 100)
	USERNAME_FIELD ="phone_number"
	REQUIRED_FIELDS = ['name','email']
	objects = UserManager()
	def __str__(self):
		return self.phone_number
	@property
	def is_staff(self):
		return self.is_admin



class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11,)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'