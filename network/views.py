from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
 


from .models import User, Post


def index(request):
    # Display all posts on the home page in reverse chronological order
    return render(request, "network/index.html", {"posts": Post.objects.all().order_by('-timestamp')})


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

@login_required(login_url='login')
def post(request):
    """
    Create a new post from a user. 
    """
    if request.method =="POST":
        post = Post()
        post.content = request.POST['content']
        post.author = request.user
        post.save()
        return HttpResponseRedirect(reverse("index"))

# Needs work, not done, but moving onto profil page. 
def like(request, post_id):
    """
    Like or unlike post then update the database
    """
    user = request.user
    post = Post.objects.get(id=post_id)
    # If user already liked, decrement the like count and remove as 'liker'
    if user in post.liked_by.all:
        post.liked_by.remove(user)
        post.likes -= 1
        post.save()
    # Else increase like count and add user    
    else:
        post.liked_by.add(user)
        post.likes += 1
        post.save 

def profile(request, username):
    # Get profile information for a user. Use iexact for case-insensitive query
    try: 
        profile = User.objects.get(username__iexact=username)
    except ObjectDoesNotExist: 
        profile = None
        return render(request, "network/profile.html", {"profile": profile})

    followers = User.objects.filter(following=profile.id)

    return render(request, "network/profile.html", {"profile": profile, "followers": followers})