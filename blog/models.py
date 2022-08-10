from django.db import models
from account.models import User
# Create your models here.
class Posts(models.Model):
	author = models.CharField(max_length= 200)
	title = models.CharField(max_length= 200)
	time_read = models.CharField(max_length= 20)
	text = models.TextField()
	date = models.DateField(auto_now_add=True)
	user_likes = models.ManyToManyField(User , related_name="post_user_likes")
	likes = models.PositiveIntegerField(default=0)
	user_dislikes = models.ManyToManyField(User , related_name="post_user_dislikes")
	dislikes = models.PositiveIntegerField(default=0)
	def __str__(self):
		return f'{self.title}'

class Comment(models.Model):
	name = models.CharField(max_length= 200)
	phone_number = models.CharField(max_length= 10)
	text = models.TextField()
	date = models.DateTimeField(auto_now_add=True )
	posts = models.ForeignKey(Posts, on_delete=models.CASCADE ,related_name="posts")
	pid = models.ForeignKey("self", on_delete=models.CASCADE,blank = True , null = True)
	user_likes = models.ManyToManyField(User , related_name="comment_user_likes")
	likes = models.PositiveIntegerField(default=0)
	user_dislikes = models.ManyToManyField(User , related_name="comment_user_dislikes")
	dislikes = models.PositiveIntegerField(default=0)
	def __str__(self):
		return f'{self.name}'