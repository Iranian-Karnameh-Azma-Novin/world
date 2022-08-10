from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , viewsets
from rest_framework.permissions import IsAuthenticated
from account.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
import random as rn
from permissions import IsOwnerOrReadOnly , admin
import requests
from django.conf.urls.static import static
from .serializers import PostsSerializer , CommentSerializer
from rest_framework.permissions import IsAdminUser
import multiprocessing as mp
import json
from django.core.paginator import Paginator
from .models import Posts , Comment
from django.http import HttpResponse
# Create your views here.





class Blog_Posts(APIView):
	#permission_classes = [IsOwnerOrReadOnly, IsAdminUser]
	serializer_class = PostsSerializer
	def post(self,request):
		ser_data = PostsSerializer(data=request.POST)
		if ser_data.is_valid():
			ser_data.save()
			return Response(ser_data.data, status=status.HTTP_201_CREATED)
		return Response({"your data is invalid"}, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk):
		posts = Posts.objects.get(pk=pk)
		posts.delete()
		return Response({'message': 'posts deleted'}, status=status.HTTP_200_OK)


	def put(self, request, pk):
		posts = Posts.objects.get(pk=pk)
		srz_data = PostsSerializer(instance=posts, data=request.data, partial=True)
		if srz_data.is_valid():
			srz_data.save()
			return Response({"updated sucessfuly"}, status=status.HTTP_200_OK)
		
		# if data was invalid
		else:
			return Response({" your values was invalid"}, status=status.HTTP_400_BAD_REQUEST)



class Get_Blog_Posts(APIView):
	#permission_classes = [IsOwnerOrReadOnly]
	serializer_class = PostsSerializer
	def get(self, request, pk = 1):
		data = self.request.query_params.dict()
		
		# if id was sent in query parts 
		try :
			id = int(data["id"])
			post = Posts.objects.get(pk=id)
			ser_data = PostsSerializer(instance= post,)
			return Response(data=ser_data.data)
		
		# if id was not sent in query parts 		
		except:
			post = Posts.objects.all()
			ser_data = PostsSerializer(instance= post,many = True)
			print("222222222222222222222222222222222222222222")
			ali = list(ser_data.data)
			#moz = ser_data.data.json()[]
			paginators = Paginator(ali, 4)
			pes = paginators.page(pk)
			return Response(data= pes.object_list )


class Blog_Comment(APIView):
	#permission_classes = [IsOwnerOrReadOnly]
	serializer_class = CommentSerializer
	def post(self,request,postid):
		parameters = {
		'name': request.POST['name'], 'phone_number': request.POST['phone_number'] , 'text' : request.POST["text"] , 'posts' : postid , 
		}
		print(parameters)
		ser_data = CommentSerializer(data=parameters,)
		if ser_data.is_valid():
			ser_data.save()
			return Response(ser_data.data, status=status.HTTP_201_CREATED)
		return Response({"your data is invalid"}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request,postid):
		data = self.request.query_params.dict()
		
		# if id was sent in query parts 
		try :
			id = int(data["id"])
			comment = Comment.objects.get(pk=id)
			ser_data = CommentSerializer(instance= comment,)
			return Response(data=ser_data.data)
		
		# if id was not sent in query parts 		
		except:
			comment = Comment.objects.filter(posts= postid)
			ser_data = CommentSerializer(instance= comment,many = True)
			return Response(data=ser_data.data)


	def delete(self, request,commentid):
		if request.user.is_admin:
			comment = Comment.objects.get(pk= commentid)
			#self.check_object_permissions(request,)
			comment.delete()
			return Response({'message': 'post deleted'}, status=status.HTTP_200_OK)
		else:
			return Response({"you are not admin "}, status=status.HTTP_400_BAD_REQUEST)

class Reply_Comment(APIView):
	#serializer_class = CommentSerializer
	permission_classes = [IsOwnerOrReadOnly]
	def post(self,request,postid,pid):
		parameters = {
		'name': request.POST['name'], 'phone_number': request.POST['phone_number'] , 'text' : request.POST["text"] , 'posts' : postid , 'pid' : pid 
		}
		ser_data = CommentSerializer(data=parameters,)
		if ser_data.is_valid():
			ser_data.save()
			return Response(ser_data.data, status=status.HTTP_201_CREATED)
		return Response({"your data is invalid"}, status=status.HTTP_400_BAD_REQUEST)


	def delete(self, request, commentid):
		if request.user.is_superuser:
			comment = Comment.objects.get(pk=commentid)
			#self.check_object_permissions(request,)
			comment.delete()
			return Response({'message': 'posts deleted'}, status=status.HTTP_200_OK)
		else:
			return Response({"you are not admin "}, status=status.HTTP_400_BAD_REQUEST)


	def get(self, request,pid):
		data = self.request.query_params.dict()
		
		# if id was sent in query parts 
		try :
			id = int(data["id"])
			comment = Comment.objects.get(pk=id)
			ser_data = CommentSerializer(instance= comment,)
			return Response(data=ser_data.data)
		
		# if id was not sent in query parts 		
		except:
			comment = Comment.objects.filter(pid= pid)
			ser_data = CommentSerializer(instance= comment,many = True)
			return Response(data=ser_data.data)





def posts_like(request, postid):
	if request.method == "POST":
		user = User.objects.filter(email= request.user)[0]
		post = Posts.objects.get(id=postid)

	#make sure can't be in dislikes
		if user in post.user_dislikes.all():
			post.user_dislikes.remove(user)
			post.user_likes.add(user)
			post.likes += 1
			post.save()
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)
	#make sure user can't like the post more than once. 
		elif (user in post.user_likes.all()):
			return HttpResponse({"you have allredy liked the post"}, status=status.HTTP_200_OK)

		else:
		#adds user to Post 
			post.likes += 1
			post.user_likes.add(user)
			post.save()
		
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)







def posts_dislike(request, postid):
	if request.method == "POST":
		user = User.objects.filter(email= request.user)[0]
		post = Posts.objects.get(id=postid)

	#make sure can't be in dislikes
		if user in post.user_likes.all():
			post.user_likes.remove(user)
			post.user_dislikes.add(user)
			post.dislikes += 1
			post.save()
			return HttpResponse({post.dislikes}, status=status.HTTP_200_OK)
	#make sure user can't like the post more than once. 
		elif (user in post.user_dislikes.all()):
			return HttpResponse({"you have allredy disliked the post"}, status=status.HTTP_200_OK)

		else:
		#adds user to Post 
			post.dislikes += 1
			post.user_dislikes.add(user)
			post.save()		
			return HttpResponse({post.dislikes}, status=status.HTTP_200_OK)





def comments_like(request, commentid):
	if request.method == "POST":
		user = User.objects.filter(email= request.user)[0]
		comment = Comment.objects.get(id=commentid)

	#make sure can't be in dislikes
		if user in comment.user_dislikes.all():
			comment.user_dislikes.remove(user)
			comment.user_likes.add(user)
			comment.likes += 1
			comment.save()
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)
	#make sure user can't like the post more than once. 
		elif (user in post.user_likes.all()):
			return HttpResponse({"you have allredy liked the post"}, status=status.HTTP_200_OK)
	#find whatever post is associated with like
		else:
		#adds user to Post 
			comment.likes += 1
			comment.user_likes.add(user)
			comment.save()
		#newLike = Like(user=user, post=post)
		#newLike.alreadyLiked = True		
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)





def comments_dislike(request, commentid):
	if request.method == "POST":
		user = User.objects.filter(email= request.user)[0]
		comment = Comment.objects.get(id=commentid)

	#make sure can't be in dislikes
		if user in comment.user_likes.all():
			comment.user_likes.remove(user)
			comment.user_dislikes.add(user)
			comment.dislikes += 1
			comment.save()
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)
	#make sure user can't like the post more than once. 
		elif (user in post.user_dislikes.all()):
			return HttpResponse({"you have allredy liked the post"}, status=status.HTTP_200_OK)

		else:
		#adds user to Post 
			comment.dislikes += 1
			comment.user_dislikes.add(user)
			comment.save()
		#newLike = Like(user=user, post=post)
		#newLike.alreadyLiked = True		
			return HttpResponse({post.likes}, status=status.HTTP_200_OK)

