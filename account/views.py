from django.shortcuts import render , redirect ,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer , OtpCodeSerializer , SetPasswordSerializer , PhoneSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User , OtpCode
from django.shortcuts import get_object_or_404
from django.views import View
import random 
from utils import send_otp_code
import multiprocessing as mp
#from permissions import IsOwnerOrReadOnly
import datetime
from datetime import timedelta
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import phonenumbers
# Create your views here.




class Signup(APIView):
	serializer_class = UserRegisterSerializer
	def post(self, request):
		request.session['user'] = {
			'password': request.POST['password'],
			'email': request.POST['email'],
			'phone_number': request.POST['phone_number'],
			'name': request.POST['name'],              
										  }
		random_code = random.randint(1000, 9999)
		phone = phonenumbers.parse(f"+98{request.POST['phone_number']}")
		if phonenumbers.is_valid_number(phone) == True :
			OtpCode.objects.create(phone_number=request.POST['phone_number'], code=random_code)
			send_otp_code(request.POST['phone_number'], random_code)
			return redirect('account:verify_code')
		else :
  			return Response({"شماره معتبر نمی باشد"})

class Verify_Code(APIView):
	serializer_class = OtpCodeSerializer
	current_time = datetime.datetime.now()
	n = 2
	future_time = current_time + timedelta(minutes = n)
	now = datetime.datetime.now()
	def post(self, request):
		user_session = request.session['user']
		code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
		code = str(code_instance.code)
		if self.future_time > self.now:
			if request.POST['code'] == code :
				code_instance.delete()
				ser_data = UserRegisterSerializer(data= user_session)
				if ser_data.is_valid():
					ser_data.create(ser_data.validated_data)
					return Response(ser_data.data, status=status.HTTP_201_CREATED)				

				#return redirect('account:moz')
			
			else :
				return Response({"your code was invalid"}, status=status.HTTP_400_BAD_REQUEST)
		else:
  			return Response({"your code has expired"}, status=status.HTTP_400_BAD_REQUEST)


def Login(request):
	follow = True		
	return redirect('http://127.0.0.1:8000/accounts/login/login/')

def Logout(request):
	return redirect('http://127.0.0.1:8000/accounts/logout/')


class New_Code(APIView):
	serializer_class = PhoneSerializer
	def post(self, request):
		random_code = random.randint(1000, 9999)
		phone = phonenumbers.parse(f"+98{request.POST['phone_number']}")
		request.session['newpass'] = {
			'phone_number': request.POST['phone_number'],
								  }
		user_phone = User.objects.get(phone_number = request.POST['phone_number'])
		if phonenumbers.is_valid_number(phone) == True :
			if user_phone:
				OtpCode.objects.create(phone_number=request.POST['phone_number'], code=random_code)
				#send_otp_code(request.POST['phone_number'], random_code)
				return redirect('account:setpassword')
			else:
	  			return Response({"شما در زمان قبل ثبت نام نکرده بودین"})			
		else :
  			return Response({"شماره معتبر نمی باشد"})


class Set_Password(APIView):
	serializer_class = OtpCodeSerializer
	current_time = datetime.datetime.now()
	n = 2
	future_time = current_time + timedelta(minutes = n)
	now = datetime.datetime.now()
	def post(self, request):
		user_session = request.session['newpass']
		code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
		code = str(code_instance.code)
		if self.future_time > self.now:
			if request.POST['code'] == code :
				code_instance.delete()
				return redirect('account:reset')
			else :
				return Response({"your code was invalid"}, status=status.HTTP_400_BAD_REQUEST)
		else:
  			return Response({"your code has expired"}, status=status.HTTP_400_BAD_REQUEST)


class New_Password(APIView):
	serializer_class = SetPasswordSerializer
	def post(self, request):
		user_session = request.session['newpass']
		user = User.objects.get(phone_number = user_session['phone_number'])
		password = request.POST["password"]
		user.set_password(password)
		#user.set_Password()
		user.save()
		return Response({"your code was invalid"}, status=status.HTTP_400_BAD_REQUEST)