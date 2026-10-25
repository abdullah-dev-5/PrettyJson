from django.contrib import admin
from django.urls import path
from . import views

app_name = 'format'

urlpatterns = [
    path('', views.home, name='home'),
    path('compare/', views.compare, name='compare'),
    
]
