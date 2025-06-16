from django.urls import path
from . import views
from django.shortcuts import render 

urlpatterns = [
    path('depo-yönetimi/', views.depo_yönetimi, name='depo_yönetimi'),
    
    path('warehouse/<int:obj_id>/edit/', views.warehouse_edit, name='warehouse_edit'),
    
    path('api/update-temperatures/', views.update_temperatures, name='update_temperatures'),
    path('api/create-warehouse/', views.create_warehouse_view, name='create_warehouse'),
]   
