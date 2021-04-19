import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post


def index(request):
    # Documentation: https://docs.djangoproject.com/en/3.0/topics/pagination/
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    # Display all posts on the home page in reverse chronological order
    return render(request, "network/index.html", {"posts": page_object})


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
    if request.method == "POST":
        post = Post()
        post.content = request.POST['content']
        post.author = request.user
        post.save()
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required(login_url='login')
def like(request, post_id):
    """
    Like or unlike post then update the database.
    """
    if request.method == "PUT":
        liked = None
        user = request.user
        post = Post.objects.get(id=post_id)
        # If user already liked, decrement the like count and remove as 'liker'
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            post.likes -= 1
            post.save()
            liked = False
        # Else increase like count and add user
        else:
            post.liked_by.add(user)
            post.likes += 1
            post.save()
            liked = True
        # Return data for updating dynamically with javascript
        return JsonResponse({"total_likes": post.likes, "liked": liked})


@csrf_exempt
@login_required(login_url='login')
def save_edit(request, post_id):
    """
    Process saving edits when user edits a post.
    """
    if request.method == "PUT":
        data = json.loads(request.body)
        user = request.user
        post = Post.objects.get(id=post_id)
        content = data.get("content", "")
        # Check to make sure user attempting edit is author
        if user == post.author:
            post.content = content
            post.save()
            return JsonResponse({"content": post.content})
        else:
            return JsonResponse({"message": "Not authorized to edit"})


def profile(request, username):
    """
    View for handling profile pages.
    """
    # Get profile information for a user. Use iexact for case-insensitive query
    try:
        profile = User.objects.get(username__iexact=username)
    except ObjectDoesNotExist:
        profile = None
        return render(request, "network/profile.html", {"profile": profile})

    # Find all users following the user whose profile being visited
    followers = User.objects.filter(following=profile.id)

    # Get posts for users and put in paginator format
    posts = Post.objects.filter(author=profile).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile": profile, "followers": followers, "posts": page_object
        })


@login_required(login_url='login')
def following(request):
    """
    Get user then determine who the user is following
    in order to grab all posts from people they follow.
    """
    user = request.user
    posts = Post.objects.filter(
                author__in=user.following.all()).order_by('-timestamp')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, "network/following.html", {"posts": page_object})


def update_followers(request, profile_id):
    """"
    Add and remove followers when button is clicked on profile page
    """
    user = request.user
    profile = User.objects.get(id=profile_id)

    if profile in user.following.all():
        user.following.remove(profile.id)
        user.save()
    else:
        user.following.add(profile.id)
        user.save()

    return HttpResponseRedirect(reverse("profile", kwargs={
        "username": profile.username
        }))
