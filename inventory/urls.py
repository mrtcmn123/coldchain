from django.urls import path
from . import views
from django.shortcuts import render 

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    
    path('all_products/', views.all_products, name='all_products'),
    path('all_products/add/', views.all_products_add, name='all_products_add'),
    path('all_products/<int:product_id>/edit/', views.all_products_edit, name='all_products_edit'),

    path('stock-movement/', views.stock_movement_list, name='stock_movement_list'),
    path('stock-movement/<int:pk>/delete/', views.delete_stock_movement, name='delete_stock_movement'),
    path('stock-movement/<int:obj_id>/edit/', views.edit_stock_movement, name='edit_stock_movement'),


    path('current-stock/', views.current_stock_view, name='current_stock'),


    path('forecast/<int:product_id>/', views.forecast_stock, name='forecast'),
    path('depletion-forecast/', views.depletion_forecast_view, name='depletion_forecast'),


    path('expiring-products/', views.expiring_products, name='expiring_products'),
    path('temperature-alert/', views.temperature_alert_view, name='temperature_alert'),

    path('export/export-all-stocks-pdf/', views.export_all_stocks_pdf, name='export_all_stocks_pdf'),
    

    path('tahminleme-dasboard/', views.tahminleme_dasboard, name='tahminleme_dasboard'),


    #------- Ajax API Endpoints -------#
    path('api/stocks/', views.stock_list_json, name='stock_list_json'), # Stokta olan urunlerin listesi

    path('api/products/', views.get_products, name='get_products'), # Product modeli icerisindeki kayitlari getirir
    path('api/warehouses/', views.get_warehouses, name='get_warehouses'), # Warehouse modeli icerisindeki kayitlari getirir
    
    path('api/create-stock/', views.create_stock, name='create_stock'), # Stock modeli icerisine yeni kayit acar

    path('api/increase-stock/', views.increase_stock, name='increase_stock'), # Stock Movement modeli icerisine yeni kayit acar
    path('api/decrease-stock/', views.decrease_stock, name='decrease_stock'), # Stock Movement modeli icerisine yeni kayit acar
    #------- (End) Ajax API Endpoints -------#


]   
