from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from profiles.models import Relationship
from radio.models import Post
from django.contrib.auth.models import User
from profiles.decorators import friendship_or_ownership_required
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_radio_view(request):
    posts = Post.objects.get_friends_and_own_posts(request.user)
    context = {
        'title' : "home",
        'posts' : posts,
    }
    return render(request, 'radio/home_radio.html', context)

@login_required
def post_upload_view(request):
    if request.method == 'POST':
        yt_code = request.POST.get('yt_code')
        post = Post(author = request.user, yt_code = yt_code)
        post.save()
        return HttpResponse("Okay")
    return HttpResponse("Error")

@login_required
def post_delete_view(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk = post_id)
        if post.author == request.user:
            post.delete()
    return redirect(reverse('radio:home_radio_view'))

@login_required
def user_radio_view(request, username):
    page_user = get_object_or_404(User, username = username)
    relationship = Relationship.objects.relationship_status(request.user, page_user)
    friend_count = Relationship.objects.get_friend_count(user = page_user)
    posts = []
    if relationship == 'friend' or relationship == 'same_person':
        posts = Post.objects.get_all_posts(page_user)
    if relationship == 'same_person':
        title = "profile"
    else: title = page_user.username
    context = {
        'title' : title,
        'page_user' : page_user,
        'relationship' : relationship,
        'friend_count' : friend_count,
        'posts' : posts,
        'post_count' : len(posts),
    }
    return render(request, 'radio/user_radio.html', context)