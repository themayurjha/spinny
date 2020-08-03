from django.contrib import admin
from django.urls import path, include
from products.views import *

urlpatterns = [
    path('', productHomeView, name='home'),
    path('add/', addBox, name='addbox'),
    path('delete/', deleteBox, name='deletebox'),
    path('update/', updateBox, name='updatebox'),
    path('allbox/', allBox, name='allbox'),
    path('mybox/', myBox, name='mybox'),
]