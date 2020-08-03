from django.contrib import admin
from django.urls import path, include
from profiles.views import *

urlpatterns = [
    path('', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
]