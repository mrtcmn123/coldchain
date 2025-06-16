from django.contrib import admin
from .models import Product, Warehouse, StockMovement
from .models import ActionLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'description')
    search_fields = ('name', 'sku')
    list_display = ['name', 'sku', 'unit', 'critical_level']



@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'temperature')
    list_filter = ('location',)




@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('movement_type', 'product', 'warehouse', 'quantity', 'timestamp', 'user')
    list_filter = ('movement_type', 'warehouse')
    search_fields = ('product__name',)



@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('action', 'user__username')