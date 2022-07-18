from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #API routes
    path("savePost", views.savePost, name="savePost"),
    path("dislike/<int:id>", views.dislike, name="dislike"),
    path("like/<int:id>", views.like, name="like")
]
