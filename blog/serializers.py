from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from .models import Posts , Comment



class PostsSerializer(serializers.ModelSerializer):
	#password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = Posts
		fields = ("author","title","time_read","text","date",)

class CommentSerializer(serializers.ModelSerializer):
	#password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = Comment
		fields = ("name","phone_number","text","date","posts","pid")
		extra_kwargs = {'pid': {'required': False} , 'posts': {'required': False}} 