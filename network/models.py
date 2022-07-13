from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Contains name, dob, about, img(url), followers(int), following(int)."""
    name = models.CharField(max_length=100,blank=True)
    dob = models.DateField(blank=True,null=True)
    about = models.TextField(max_length=1000,blank=True)
    img = models.URLField(blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username} created"

class Posts(models.Model):
    """Contains user, time(auto_now_add), content, likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_posts")
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000,null=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} created a post."

class Following(models.Model):
    """follower -> followed"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.follower} follows {self.followed}."
    class Meta:
     unique_together = ('follower', 'followed',)