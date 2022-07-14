from distutils.log import error
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Following, User, Post
import json
from django.contrib.auth.decorators import login_required


def index(request):
   if request.method == "POST":
      content = request.POST["tweet"]
      user_id = request.POST["user_id"]
      user = User.objects.get(id=user_id)
      q = Post(user=user,content=content)
      q.save()
      return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("-time")
      })
   else:
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by("-time")
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def profile(request,id):

    if request.method == "POST":
        res = request.POST["res"]
        profile = User.objects.get(pk=id)
        posts = Post.objects.filter(user=profile)
        current_user = User.objects.get(pk=request.user.id)

        if res == "follow":
           q = Following(follower=request.user,followed=profile)
           q.save()
           profile.followers += 1
           profile.save()
           current_user.following += 1
           current_user.save()
        else:
            Following.objects.filter(follower=request.user,followed=profile).delete()
            profile.followers -= 1
            profile.save()
            current_user.following -= 1
            current_user.save()
        return HttpResponseRedirect(reverse("profile", args=(id,)))
 

    else:
         profile = User.objects.get(pk=id)
         posts = Post.objects.filter(user=profile)
         print(posts)
         val = False

         try:
            q = Following.objects.filter(follower=request.user,followed=profile)
            if len(q) >= 1:
               val = True
            else:
               val = False
         except: 
             print("error")
            
         return render(request, "network/profile.html",{
          "profile": profile,
          "posts": posts,
          "val": val
         })


def following(request):
    list_users = Following.objects.filter(follower=request.user)
    list = []
    for x in list_users:
        list.append(x.followed)

    post = Post.objects.filter(user__in=list)
    return render(request, "network/posts.html", {
        "posts": post
    })