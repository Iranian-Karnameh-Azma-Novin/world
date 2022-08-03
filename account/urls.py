from django.contrib import admin
from django.urls import path , include
from rest_framework import routers
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views




app_name = 'account'
urlpatterns = [
 # !!!  this is for register page and we create our user in this view
    path("signup",views.Signup.as_view(),name = "signup"),
    path("signup/verify",views.Verify_Code.as_view(),name = "verify_code"),
    path("logins",views.Login,name = "login"),
	path("login/",include ("django.contrib.auth.urls"),),
    path("logout",views.Logout,name = "logout"),
]
