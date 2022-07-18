from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Following, User, Post, Like
import json
from django.contrib.auth.decorators import login_required
import json


def index(request):
   if request.method == "POST":
      content = request.POST["tweet"]
      user_id = request.POST["user_id"]

      if content == None or content == "":
        return HttpResponse("Empty Tweet not allowed!!")
      
      user = User.objects.get(id=user_id)
      q = Post(user=user,content=content)
      q.save()
       
      return HttpResponseRedirect(reverse("index"))
   else:
     likes = []
     try:
         likes = Like.objects.filter(user=request.user)
     except:
         print("logged out user")

     list_like = []
     for like in likes:
        list_like.append(like.post.id)

     print(list_like)
     posts = Post.objects.all().order_by("-time")
     paginator = Paginator(posts, 10)
     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     return render(request, "network/index.html", {
         "posts": page_obj,
         "likes": list_like,
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
         likes = []
         try:
              likes = Like.objects.filter(user=request.user)
         except:
              print("logged out user")

         list_like = []
         for like in likes:
             list_like.append(like.post.id)

         print(list_like)
         profile = User.objects.get(pk=id)
         posts = Post.objects.filter(user=profile).order_by("-time")
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

         paginator = Paginator(posts, 10)
         page_number = request.GET.get('page')
         page_obj = paginator.get_page(page_number)    
            
         return render(request, "network/profile.html",{
          "profile": profile,
          "posts": page_obj,
          "val": val,
          "likes": list_like,
         })


def following(request):
   
    likes = []
    try:
         likes = Like.objects.filter(user=request.user)
    except:
         print("logged out user")

    list_like = []
    for like in likes:
        list_like.append(like.post.id)

    print(list_like)

    list_users = Following.objects.filter(follower=request.user)
    list = []
    for x in list_users:
        list.append(x.followed)

    post = Post.objects.filter(user__in=list).order_by("-time")
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/posts.html", {
        "posts": page_obj,
        "likes": list_like,
    })

def savePost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        Post.objects.filter(id=data["post_id"]).update(content=data["content"])
        return HttpResponse("Updated Successfully", status=200)
    
@login_required(login_url="login")
def like(request,id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        post.likes += 1
        post.save()
        l = Like(user=user, post=post)
        l.save()
        return HttpResponse("Increased Likes Successfully", status=200)

@login_required(login_url="login")
def dislike(request,id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        post.likes -= 1
        post.save()
        Like.objects.filter(post=post,user=user).delete()
        return HttpResponse("Decreased Likes Successfully", status=200)
    