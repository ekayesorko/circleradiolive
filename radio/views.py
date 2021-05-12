from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
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

@friendship_or_ownership_required
def user_radio_view(request, username):
    user = get_object_or_404(User, username = username)
    posts = Post.objects.get_all_posts(user)
    print(posts)
    context = {
        'title' : "profile",
        'posts' : posts
    }
    return render(request, 'radio/user_radio.html', context)