from django.core.exceptions import PermissionDenied
from .models import Relationship
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse

def friendship_or_ownership_required(function):
    def wrap(request, *args, **kwargs):
        another_username = kwargs['username']
        another_user = User.objects.get(username = another_username)
        if(Relationship.objects.friend_existence_check(another_user, request.user) or
            another_user == request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def login_forbidden(function):
    def wrap(request, *args, **kwargs):
        if (request.user.is_authenticated):
            return redirect(reverse('radio:home_radio_view'))
        else:
            return function(request, *args, **kwargs)
    return wrap