from django.urls import path
from . import views

urlpatterns = [
    path('', views.ayarlar, name='ayarlar'),
]   
