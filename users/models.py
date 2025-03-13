from django.db import models
from django.contrib.auth.models import User


import uuid
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True,null=True, blank=True)
    username = models.CharField(max_length=200,null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True,null=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    favorites = models.ManyToManyField('reviews.Anime', related_name='favorited_by', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower','following')

    def __str__(self):
        return f'{self.follower.user.username} - {self.following.user.username}'