from django.urls import path
from radio.views import (
    home_radio_view, post_upload_view, user_radio_view
)


app_name = 'radio'

urlpatterns = [
    path('', home_radio_view, name = 'home_radio_view'),
    path('post_upload', post_upload_view, name = 'post_upload_view'),    
    path('user/<str:username>/', user_radio_view, name = 'user_radio_view'),
]
