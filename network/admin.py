from django.contrib import admin
from .models import Following, Like, Post, User

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Following)
admin.site.register(Like)