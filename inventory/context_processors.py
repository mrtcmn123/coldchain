from django.utils.timezone import now, timedelta
from django.db.models import F
from .models import Stock

def user_alerts(request):
    alerts = []

    # Tarih hesapla (30 gün sonrası)
    warning_date = now().date() + timedelta(days=30)

    # SKT yaklaşanlar
    expiring_soon = Stock.objects.filter(expiration_date__lte=warning_date)
    for stock in expiring_soon:
        alerts.append({
            "message": f"{stock.product.name} ürününün SKT tarihi yaklaşıyor",
            "link": "/inventory/current-stock/?filter=expiring"
        })

    # Sıcaklık aşımları
    violating_stocks = Stock.objects.select_related("warehouse", "product").filter(
        warehouse__temperature__lt=F('product__min_temperature')
    ) | Stock.objects.select_related("warehouse", "product").filter(
        warehouse__temperature__gt=F('product__max_temperature')
    )

    for stock in violating_stocks:
        alerts.append({
            "message": f"{stock.product.name} ürünü sıcaklık sınırlarını aşıyor",
            "link": "/inventory/temperature-alert/"  # 🔁 Burada sabit olarak bu linki veriyoruz
        })

    return {'user_alerts': alerts}
