from django.contrib.postgres import search
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Relationship
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from profiles.decorators import login_forbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.db.models.functions import Greatest

# Create your views here.
@login_required
def friends_view(request):
    all_user_list = User.objects.all()
    people_you_may_know = []
    for user in all_user_list:
        if (Relationship.objects.relation_existence_check(user, request.user) == False) and (user != request.user):
            people_you_may_know.append(user)
    
    friend_request_list = Relationship.objects.get_friend_request_list(request.user)
    sent_friend_request_list = Relationship.objects.get_sent_friend_request_list(request.user)
    friend_list = Relationship.objects.get_friend_list(request.user)
    user_profile = Profile.objects.get(user = request.user)
    context = {
        'title' : "friends",
        'people_you_may_know' : people_you_may_know,
        'friend_request_list' : friend_request_list,
        'sent_friend_request_list' : sent_friend_request_list,
        'friend_list' : friend_list,
        'user_profile' : user_profile
    }
    return render(request, 'profiles/friends_view.html', context)

@login_forbidden
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user = user)
            return redirect(reverse('radio:home_radio_view'))
    return render(request, 'profiles/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('profiles:login_view'))

@login_forbidden
def signup_view(request):
    signup_form = SignupForm()
    context = {
        'form' : signup_form,
    }
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            user = User.objects.get(username = username)
            Profile.objects.create(user = user)
            return redirect(reverse('profiles:login_view'))
        else:
            messages.error(request, "Invalid Data")
    return render(request, 'profiles/signup.html', context = context)

@csrf_exempt
def username_availability_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if len(username) < 4:
            return HttpResponse("false")
        if User.objects.filter(username = username).exists():
            return HttpResponse("false")
        else: return HttpResponse("true")

@login_required
def add_friend_view(request):
    if request.method == 'POST':
        sender = request.user
        receiver_username = request.POST.get('receiver_username')
        print(receiver_username)
        receiver = User.objects.get(username = receiver_username)
        Relationship.objects.send_friend_request(sender, receiver)
    return redirect(reverse('profiles:friends_view'))

@login_required
def remove_friend_view(request):
    if request.method == 'POST':
        friend_username = request.POST.get('friend_username')
        friend = User.objects.get(username = friend_username)
        Relationship.objects.remove_relationship(friend, request.user)
    return redirect(reverse('profiles:friends_view'))

@login_required
def accept_friend_view(request):
    if request.method == 'POST': 
        friend_username = request.POST.get('friend_username')
        friend = User.objects.get(username = friend_username)
        Relationship.objects.accept_friend_request(friend, request.user)
    return redirect(reverse('profiles:friends_view'))

@login_required
def search_friend_view(request):
    query_string = request.GET.get('query_string')
    user_list = User.objects.annotate(
        search = SearchVector('username', 'first_name', 'last_name')
    ).filter(search = query_string)
    relation_list = []
    for user in user_list:
        relation_list.append(
            Relationship.objects.relationship_status(request.user, user)
        )
    print(len(relation_list))
    user_data = zip(user_list, relation_list)
    context = {
        'user_data' : user_data,
    }
    return render(request, 'profiles/search_friend_view.html', context)

@login_required
def edit_profile_view(request):
    profile = Profile.objects.get(user = request.user)
    return HttpResponse(profile)

    