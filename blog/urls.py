from django.contrib import admin
from django.urls import path , include
from . import views



app_name = 'blog'
urlpatterns = [
	path("blog_posts/post",views.Blog_Posts.as_view()),
	path("blog_posts/get/<int:pk>",views.Get_Blog_Posts.as_view()),
	path("blog_posts/delete/<int:pk>",views.Blog_Posts.as_view()),
	path("blog_posts/put/<int:pk>",views.Blog_Posts.as_view()),
	path("blog_comment/post/<int:postid>",views.Blog_Comment.as_view()),
	path("blog_comment/get/<int:postid>",views.Blog_Comment.as_view()),
	path("blog_comment/delete/<int:postid>",views.Blog_Comment.as_view()),
	path("blog_comment/reply/post/<int:postid>/<int:pid>",views.Reply_Comment.as_view()),
	path("blog_comment/reply/get/<int:pid>",views.Reply_Comment.as_view()),
	path("blog_comment/reply/delete/<int:pid>",views.Reply_Comment.as_view()),
	path("blog_posts/like/<int:postid>",views.posts_like),
	path("blog_posts/dislike/<int:postid>",views.posts_dislike),
	path("blog_comment/like/<int:commentid>",views.comments_like),
	path("blog_comment/dislike/<int:commentid>",views.comments_dislike),
]
