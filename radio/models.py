from django.db import models
from profiles.models import Relationship
from django.contrib.auth.models import User
# Create your models here.

class PostManager (models.Manager):
    def get_all_posts(self, author):
        posts = Post.objects.filter(author = author)
        return posts

    def get_friends_and_own_posts(self, user):
        all_friends = Relationship.objects.get_friend_list(user)
        total_post = 50
        posts = Post.objects.filter(author = user) #init with own post
        for friend in all_friends:
            friend_posts = Post.objects.filter(author = friend)
            posts = posts.union(friend_posts)
        return posts.order_by('-time')[:total_post]
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    yt_code = models.CharField(max_length=11)
    time = models.DateTimeField(auto_now_add = True)
    objects = PostManager()

    def __str__(self):
        return self.yt_code
    

