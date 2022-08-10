from rest_framework import serializers
from .models import User , OtpCode
from django.contrib.auth import get_user_model

def clean_email(value):
	if 'admin' in value:
		raise serializers.ValidationError('admin cant be in email')

class UserRegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('name', 'email', 'password','phone_number')
		extra_kwargs = {
			'password': {'write_only':True},
			'email': {'validators': (clean_email,)}
		}

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

	def validate_name(self, value):
		if value == 'admin':
			raise serializers.ValidationError('username cant be `admin`')
		return value

	'''
	def validate(self, data):
		if data['password'] != data['password2']:
			raise serializers.ValidationError('passwords must match')
		return data
		'''

class OtpCodeSerializer(serializers.ModelSerializer):

	class Meta:
		model = OtpCode
		fields = ('code',)


class PhoneSerializer(serializers.ModelSerializer):

	class Meta:
		model = OtpCode
		fields = ('phone_number',)



class SetPasswordSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('password',)
		extra_kwargs = {
			'password': {'write_only':True},
		}