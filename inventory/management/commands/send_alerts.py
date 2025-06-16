from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from inventory.models import Product, Warehouse, StockMovement, Stock
from django.db.models import Sum
from datetime import date, timedelta

# class Command(BaseCommand):
#     help = 'Kritik stok, SKT ve sıcaklık uyarılarını maille gönderir'

#     def handle(self, *args, **options):
#         warning_date = date.today() + timedelta(days=7)
#         to_email = ['yonetici@mail.com']  # Hedef kullanıcılar

#         # Kritik stoklar
#         kritiks = []
#         for product in Product.objects.all():
#             in_qty = StockMovement.objects.filter(product=product, movement_type='IN').aggregate(Sum('quantity'))['quantity__sum'] or 0
#             out_qty = StockMovement.objects.filter(product=product, movement_type='OUT').aggregate(Sum('quantity'))['quantity__sum'] or 0
#             total = in_qty - out_qty
#             if total <= product.critical_level:
#                 kritiks.append(f"{product.name} - {total} adet")

#         # SKT yaklaşanlar
#         skts = Stock.objects.filter(expiration_date__lte=warning_date)

#         # Yüksek sıcaklık
#         hot_depos = Warehouse.objects.filter(temperature__gt=8)

#         # Mail içeriği
#         body = "📉 Kritik Stoklar:\n"
#         body += '\n'.join(kritiks) if kritiks else "Yok\n"

#         body += "\n📅 SKT Yaklaşan Ürünler:\n"
#         body += '\n'.join([f"{s.product.name} ({s.expiration_date})" for s in skts]) if skts else "Yok\n"

#         body += "\n🌡️ Yüksek Sıcaklıkta Depolar:\n"
#         body += '\n'.join([f"{w.name} ({w.temperature}°C)" for w in hot_depos]) if hot_depos else "Yok\n"

#         send_mail(
#              subject="Uyarı",
#              message="Deneme mailidir",
#              from_email=None,
#              recipient_list=["cimenmert7@gmail.com"],
#              fail_silently=False  
#         )

#         self.stdout.write(self.style.SUCCESS("Mail gönderildi."))
