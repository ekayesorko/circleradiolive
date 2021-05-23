from django.urls import path
from .views import (friends_view, login_view, signup_view, logout_view, add_friend_view,
    remove_friend_view, accept_friend_view, username_availability_view, search_friend_view, edit_profile_view
)


app_name = 'profiles'

urlpatterns = [
    path('friends/', friends_view, name = 'friends_view'),
    path('login/', login_view, name = 'login_view'),
    path('signup/', signup_view, name = 'signup_view'),
    path('logout/', logout_view, name = 'logout_view'),
    path('add_friend/', add_friend_view, name = 'add_friend_view'),
    path('remove_friend/', remove_friend_view, name = 'remove_friend_view'),
    path('accept_friend/', accept_friend_view, name = 'accept_friend_view'),
    path('username_available/', username_availability_view, name = 'username_availability_view'),
    path('search_friend', search_friend_view, name = 'search_friend_view' ),
    path('edit_profile/', edit_profile_view, name = 'edit_profile_view'),
]
