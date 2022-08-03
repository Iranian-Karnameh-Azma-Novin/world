from django.contrib.auth.models import BaseUserManager
from .models import User

class UserManager(BaseUserManager):
	User = User()
	def create_user(self, phone_number, email , name, password):
		if not phone_number:
			raise ValueError('user must have phone number')

		if not email:
			raise ValueError('user must have email')

		if not name:
			raise ValueError('user must have full name')

		User = self.model(phone_number=phone_number, email = email, name= name)
		User.set_password(password)
		User.save(using=self._db)
		return User

	def create_superuser(self, phone_number, email, name, password):
		user = self.create_user(phone_number, email, name, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
