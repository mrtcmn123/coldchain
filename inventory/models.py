from django.db import models
from django.contrib.auth.models import User

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    temperature = models.FloatField(help_text="Depo sıcaklığı (°C)")
    
    
    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('adet', 'Adet'),
        ('kilo', 'Kilo'),
        ('koli', 'Koli'),
        ('palet', 'Palet'),
        ('çuval', 'Çuval'),
        ('kasa', 'Kasa'),
        ('teneke', 'Teneke'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Ürün Adı')
    sku = models.CharField(max_length=50)  
    description = models.TextField(blank=True)
    critical_level = models.PositiveIntegerField(default=10, verbose_name='Minimum Stok Eşiği')
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='adet', verbose_name='Birim')

    min_temperature = models.FloatField(null=True, blank=True, verbose_name='Minimum Sıcaklık (°C)')
    max_temperature = models.FloatField(null=True, blank=True, verbose_name='Maksimum Sıcaklık (°C)')

    is_active = models.BooleanField(default=True)  # 👈 SOFT DELETE ALANI EKLE

    def __str__(self):
        return f"{self.name} / {self.sku}"
    

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"Urun-{self.id}"

        super().save(*args, **kwargs)




class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.product.name} – {self.warehouse.name} – SKT: {self.expiration_date.strftime('%d.%m.%Y')}"



class StockMovement(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    MOVEMENT_TYPE_CHOICES = [
        (IN, 'Giriş'),
        (OUT, 'Çıkış'),
    ]

    stock_obj = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='movements')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.timestamp.strftime('%Y-%m-%d')}"


class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"