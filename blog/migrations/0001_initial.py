# Generated by Django 4.0.6 on 2022-08-03 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('time_read', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('user_dislikes', models.ManyToManyField(related_name='post_user_dislikes', to=settings.AUTH_USER_MODEL)),
                ('user_likes', models.ManyToManyField(related_name='post_user_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=10)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.posts')),
                ('user_dislikes', models.ManyToManyField(related_name='comment_user_dislikes', to=settings.AUTH_USER_MODEL)),
                ('user_likes', models.ManyToManyField(related_name='comment_user_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
