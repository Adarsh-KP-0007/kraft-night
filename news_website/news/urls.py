from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home-view'),
    path('signup/',user_register,name='signup'),
    path('login/',user_login,name='login'),
    path('news/',news_display,name='display-news'),
    path('logoutUser/',logoutUser,name='logout-user')
]