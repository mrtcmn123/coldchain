from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db.models import Sum
from datetime import date, timedelta, datetime
from .models import Product
from django.shortcuts import get_object_or_404
from .models import Product, Warehouse, StockMovement, Stock, ActionLog
from django.contrib import messages
from django import forms
from django.db.models import F
from reportlab.pdfgen import canvas
from django.http import JsonResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io, base64
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from .forms import StockMovementForm, ProductForm
from collections import defaultdict



from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.db import transaction
from urllib.parse import unquote
from django.db.models import Q, F

from datetime import timedelta
from django.utils import timezone


import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import A4


@login_required
def all_products(request):

    product_list = Product.objects.all()

    search_query = request.GET.get("q")

    if search_query:
        product_list = product_list.filter(name__icontains=search_query)
    
    ## ----------------- 1. Calistirilacak kod

    # products_data = [
    #     ("Kuru İncir Kasa", 189),
    #     ("Kuru İncir Bidon", 173),
    #     ("Kudüs Hurma Jumbo", 320),
    #     ("Kudüs Hurma Large", 169),
    #     ("Kudüs Hurma Medium", 0),
    #     ("Medine Hurma", 0),
    #     ("Tunus Hurma", 191),
    #     ("Kabuklu Ceviz (10kg)", 0),
    #     ("Kabuklu Ceviz (25kg)", 330),
    #     ("Çeyrek Ceviz", 0),
    #     ("Kaju 180", 0),
    #     ("Kaju 210", 0),
    #     ("Kaju 240", 0),
    #     ("Kaju 320", 0),
    #     ("Kaju Zarlı", 79),
    #     ("Kaju Pirinç", 327),
    #     ("Bertina Badem", 62),
    #     ("Datça Badem", 0),
    #     ("Kırık Bertina Badem", 18),
    #     ("Amerikan Badem 20-22", 170),
    #     ("Almendras Badem", 0),
    #     ("Alligna Farms Badem", 0),
    #     ("Promosyon Badem", 0),
    #     ("Promosyon Badem Küçük", 0),
    #     ("AH 24 Badem", 110),
    #     ("Şak Fıstık", 22),
    #     ("Tutti Furitti", 16),
    #     ("PopCorn", 48),
    #     ("Hünnap", 30),
    #     ("Akkabak", 132),
    #     ("Cennet Hurması", 790),
    #     ("Kırmızı erik", 0),
    # ]

    # for name, dummy_qty in products_data:
    #     Product.objects.create(
    #         name=name,
    #         critical_level=50,
    #         unit=random.choice(['kilo', 'kasa', 'adet']),
    #         min_temperature=2.0,
    #         max_temperature=12.0
    #     )


    # # ----------------- 2. Calistirilacak kod
    # StockMovement.objects.all().delete()  # Mevcut stokları temizle
    # Stock.objects.all().delete()  # Mevcut stokları temizle

    # fake = Faker()

    # user = User.objects.first()
    # warehouse_ids = list(Warehouse.objects.values_list('id', flat=True))
    # product_ids = list(Product.objects.values_list('id', flat=True))

    # stock_objects = []
    # movement_objects = []

    # # Bazı ürünler için çıkış oranı yüksek olsun (yaklaşık %30'u)
    # high_out_products = set(random.sample(product_ids, k=max(1, len(product_ids) // 9)))  # ~%30

    # for _ in range(45):  # 30 farklı stok
    #     product_id = random.choice(product_ids)
    #     product = Product.objects.get(id=product_id)
    #     warehouse = Warehouse.objects.get(id=random.choice(warehouse_ids))
    #     quantity = random.randint(20, 300)
    #     expiration_date = fake.date_between(start_date="+15d", end_date="+180d")

    #     stock = Stock.objects.create(
    #         product=product,
    #         warehouse=warehouse,
    #         quantity=quantity,
    #         expiration_date=expiration_date
    #     )
    #     stock_objects.append(stock)

    #     for _ in range(random.randint(5, 20)):
    #         if product_id in high_out_products:
    #             is_in = random.choices([True, False], weights=[5, 95])[0]  # Çıkış ağırlıklı
    #         else:
    #             is_in = random.choices([True, False], weights=[95, 5])[0]  # Giriş ağırlıklı

    #         move_qty = random.randint(5, 80)

    #         movement = StockMovement.objects.create(
    #             stock_obj=stock,
    #             product=product,
    #             warehouse=warehouse,
    #             quantity=move_qty if is_in else -move_qty,
    #             movement_type="IN" if is_in else "OUT",
    #             timestamp=fake.date_time_between(start_date="-3M", end_date="now"),
    #             user=user,
    #             expiration_date=expiration_date
    #         )
    #         movement_objects.append(movement)

    # print(f"{len(stock_objects)} stok ve {len(movement_objects)} hareket başarıyla oluşturuldu.")





    return render(request, 'inventory/all_products.html', {
        'product_list': product_list,
        'search_query': search_query,
    })




@login_required
def all_products_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Product.objects.filter(name=name).exists():
                messages.warning(request, "⚠️ Bu isimde bir ürün zaten var.")
            else:
                form.save()
                messages.success(request, "✅ Ürün başarıyla eklendi.")
                return redirect('all_products')
    else:
        form = ProductForm()

    return render(request, 'inventory/all_products_add.html', {
        'form': form
    })






@login_required
def all_products_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if request.POST.get('delete_product') == '1':
            product.delete()
            messages.success(request, "🗑️ Ürün tamamen silindi.")
            return redirect('all_products')
        
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Ürün başarıyla güncellendi.")
            return redirect('all_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/all_products_edit.html', {
        'form': form
    })


    

def stock_list_json(request):
    stocks = Stock.objects.select_related('product', 'warehouse')

    if not stocks.exists():
        return JsonResponse({'status': 'empty', 'message': 'Stok kaydı bulunamadı.'})

    
    data = []
    for stock in stocks:
        data.append({
            'id': stock.id,
            'product': stock.product.name,
            'warehouse': stock.warehouse.name,
            'quantity': stock.quantity,
            'label': f"{stock.product.name} / {stock.warehouse.name} / {stock.quantity}"
        })
    return JsonResponse(data, safe=False)



@login_required(login_url="accounts:login")
def get_products(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            products = Product.objects.all().values('id', 'name')
            product_list = list(products)

            print(f"Product list: {product_list}")  # Debugging için konsola yazdır

            return JsonResponse({
                'alert': 1,
                'products': product_list
            })
        except Exception as e:
            return JsonResponse({
                'alert': 0,
                'error': str(e)
            }, status=400)
    # Geçersiz istek
    return JsonResponse({'alert': 2})  # geçersiz istek




@login_required(login_url="accounts:login")
def get_warehouses(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            warehouses = Warehouse.objects.all().values('id', 'name')
            data = list(warehouses)
            return JsonResponse({
                'alert': 1,
                'warehouses': data
            })
        except Exception as e:
            return JsonResponse({
                'alert': 0,
                'error': str(e)
            }, status=400)
    return JsonResponse({'alert': 2})  # Geçersiz istek


@require_POST
@csrf_exempt  # modal dışı formdaysa geçici olarak bunu ekleyebilirsin
def create_stock(request):
    product_id = request.POST.get('product_id')
    warehouse_id = request.POST.get('warehouse_id')
    expiration_date = request.POST.get('expiration_date')
    quantity = request.POST.get('quantity')

    try:
        if not Stock.objects.filter(product_id=product_id, warehouse_id=warehouse_id).exists():
            stock = Stock.objects.create(
                product_id=product_id,
                warehouse_id=warehouse_id,
                expiration_date=parse_date(expiration_date),
                quantity=int(quantity)
            )

            StockMovement.objects.create(
                stock_obj=stock,
                product=stock.product,
                warehouse=stock.warehouse,
                quantity=int(quantity),
                movement_type='IN',
                expiration_date=stock.expiration_date,
                user=request.user
            )
        

            messages.success(request, "✅ Ürün başarıyla oluşturuldu.")
            return JsonResponse({'success': True, 'redirect_url': '/inventory/current-stock/'})
    
        else:
            return JsonResponse({'success': False, 'error': 'Bu kayit zaten mevcut'}, status=400)
    

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    


@require_POST
@csrf_exempt  # CSRF token AJAX ile çözülene kadar geçici
def increase_stock(request):
    stock_id = request.POST.get('stock_id')
    quantity = request.POST.get('quantity')

    try:
        stock_obj = Stock.objects.filter(id=stock_id).first()

        if not stock_obj:
            return JsonResponse({'success': False, 'error': 'Stok bulunamadı.'}, status=404)

        try:
            qty_to_add = int(quantity)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Geçersiz miktar.'}, status=400)

        if qty_to_add <= 0:
            return JsonResponse({'success': False, 'error': 'Miktar pozitif olmalıdır.'}, status=400)

        stock_obj.quantity += qty_to_add
        stock_obj.save()

        StockMovement.objects.create(
            stock_obj=stock_obj,
            product=stock_obj.product,
            warehouse=stock_obj.warehouse,
            quantity=int(quantity),
            movement_type='IN',
            expiration_date=stock_obj.expiration_date,
            user=request.user
        )
        
        messages.success(request, "✅ Stok başarıyla arttırıldı.")
        return JsonResponse({'success': True, 'redirect_url': '/inventory/current-stock/'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



@require_POST
@csrf_exempt  # modal dışı formdaysa geçici olarak bunu ekleyebilirsin
def decrease_stock(request):
    stock_id = request.POST.get('stock_id')
    quantity = request.POST.get('quantity')

    try:
        stock_obj = Stock.objects.filter(id=stock_id).first()

        if not stock_obj:
            return JsonResponse({'success': False, 'error': 'Stok bulunamadı.'}, status=404)

        try:
            qty_to_decrease = int(quantity)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Geçersiz miktar.'}, status=400)

        if qty_to_decrease <= 0:
            return JsonResponse({'success': False, 'error': 'Miktar pozitif olmalıdır.'}, status=400)

        if stock_obj.quantity < qty_to_decrease:
            return JsonResponse({'success': False, 'error': 'Yetersiz stok miktarı.'}, status=400)

        stock_obj.quantity -= qty_to_decrease
        stock_obj.save()


        StockMovement.objects.create(
            stock_obj=stock_obj,
            product=stock_obj.product,
            warehouse=stock_obj.warehouse,
            quantity=int(quantity),
            movement_type='OUT',
            expiration_date=stock_obj.expiration_date,
            user=request.user
        )


        messages.success(request, "✅ Stok başarıyla azaltıldı.")
        return JsonResponse({'success': True, 'redirect_url': '/inventory/current-stock/'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)





@login_required
def current_stock_view(request):
    search_query = request.GET.get("q", "")
    filter_type = request.GET.get("filter", None)

    all_stocks = Stock.objects.select_related("product", "warehouse")

    # Filtrelenmiş listeyi oluştur
    filtered_stocks = []

    for stock in all_stocks:
        # Arama varsa ürün adına göre filtrele
        if search_query and search_query.lower() not in stock.product.name.lower():
            continue

        # Kritik stok
        if filter_type == "critical":
            # Ürün bazlı stok miktarlarını topla
            product_totals = defaultdict(int)
            product_to_stocks = defaultdict(list)

            for stock in all_stocks:
                product_totals[stock.product] += stock.quantity
                product_to_stocks[stock.product].append(stock)

            # Kritik stok seviyesinin altında kalan ürünlere ait stokları topla
            for product, total_qty in product_totals.items():
                if total_qty <= product.critical_level:
                    filtered_stocks.extend(product_to_stocks[product])


        # SKT yaklaşan
        elif filter_type == "expiring":
            if stock.expiration_date and timezone.now().date() <= stock.expiration_date <= timezone.now().date() + timedelta(days=30):
                filtered_stocks.append(stock)

        # Filtre yoksa hepsini al
        elif not filter_type:
            filtered_stocks.append(stock)



    # Hazırlanacak veri
    stock_data = []
    for stock in filtered_stocks:
        movements = StockMovement.objects.filter(stock_obj=stock).select_related('user').order_by('-timestamp')

        movement_list = []
        for mv in movements:
            movement_list.append({
                'mv_id': mv.id,
                'movement_type': mv.movement_type,
                'quantity': mv.quantity,
                'timestamp': mv.timestamp.strftime('%Y-%m-%d %H:%M'),
                'user': mv.user.get_full_name() or mv.user.username
            })

        stock_data.append({
            'product': stock.product.name,
            'warehouse': stock.warehouse.name,
            'quantity': stock.quantity,
            'expiration_date': stock.expiration_date.strftime('%Y-%m-%d') if stock.expiration_date else '—',
            'movements': movement_list,
            'temp_aralik': f"{stock.product.min_temperature}°C - {stock.product.max_temperature}°C" if stock.product.min_temperature is not None and stock.product.max_temperature is not None else "—"

        })

    return render(request, 'inventory/current_stock.html', {
        'stock_data': stock_data,
        'search_query': search_query
    })






from collections import defaultdict
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import Product, Stock, StockMovement




@login_required
def tahminleme_dasboard(request):
    products = Product.objects.filter(is_active=True)
    stocks = Stock.objects.select_related('product')
    movements = StockMovement.objects.filter(
        movement_type="OUT",
        timestamp__gte=timezone.now() - timedelta(days=90)
    ).select_related('product')

    product_stock_map = defaultdict(int)
    for stock in stocks:
        product_stock_map[stock.product.id] += stock.quantity

    movement_stats = defaultdict(lambda: {'total_out': 0, 'first': None, 'last': None})
    for mv in movements:
        pid = mv.product.id
        movement_stats[pid]['total_out'] += abs(mv.quantity)
        if not movement_stats[pid]['first'] or mv.timestamp < movement_stats[pid]['first']:
            movement_stats[pid]['first'] = mv.timestamp
        if not movement_stats[pid]['last'] or mv.timestamp > movement_stats[pid]['last']:
            movement_stats[pid]['last'] = mv.timestamp

    prediction_data = []
    for product in products:
        pid = product.id
        current_stock = product_stock_map.get(pid, 0)

        if pid in movement_stats and movement_stats[pid]['total_out'] > 0:
            total_days = (movement_stats[pid]['last'] - movement_stats[pid]['first']).days or 1
            daily_out = movement_stats[pid]['total_out'] / total_days
            days_left = int(current_stock / daily_out) if daily_out > 0 else None
        else:
            daily_out = 0
            days_left = None

        prediction_data.append({
            "product": product,
            "current_stock": current_stock,
            "daily_out_avg": round(daily_out, 2),
            "days_left": days_left
        })

    # Sıralama
    sort_field = request.GET.get("sort", "days_left")
    sort_order = request.GET.get("order", "asc")

    def get_sort_key(item):
        value = item.get(sort_field)

        if sort_field == "days_left":
            if value is None:
                return float('inf') if sort_order == "asc" else float('-inf')
            return value

        return value if value is not None else float('inf')

    reverse = sort_order == "desc"
    prediction_data = sorted(prediction_data, key=get_sort_key, reverse=reverse)

    return render(request, 'inventory/tahminleme_dasboard.html', {
        'prediction_data': prediction_data,
        'current_sort': sort_field,
        'current_order': sort_order,
    })





@login_required
def stock_movement_list(request):
    stock_movement_list = StockMovement.objects.all()


    return render(request, 'inventory/stock_movement_list.html', {
        'stock_movement_list': stock_movement_list
    })




@login_required
@permission_required('inventory.delete_product', raise_exception=True)
def delete_stock_movement(request, pk):

    product = get_object_or_404(Product, pk=pk)
    product.is_active = False  # ❌ Fiziksel silme yok, sadece pasif yap
    product.save()
    messages.success(request, f"🗑️ '{product.name}' başarıyla silindi.")
    return redirect('stock_movement_list')




def recalculate_stock_quantity(product, warehouse):
    """
    Verilen Stock nesnesinin tüm hareketlerini (StockMovement)
    değerlendirerek quantity alanını sıfırdan hesaplar ve günceller.
    """

    try:
        stock = Stock.objects.get(product=product, warehouse=warehouse)
    except Stock.DoesNotExist:
        return None  # veya raise

    movements = StockMovement.objects.filter(product=product, warehouse=warehouse)
    total = 0

    for mv in movements:
        if mv.movement_type == 'IN':
            total += mv.quantity
        elif mv.movement_type == 'OUT':
            total -= mv.quantity

    stock.quantity = total
    stock.save()
    return stock




@login_required
def edit_stock_movement(request, obj_id):
    sm_obj = get_object_or_404(StockMovement, id=obj_id)
    original_qty = sm_obj.quantity
    original_type = sm_obj.movement_type
    stock_obj = sm_obj.stock_obj

    next_url = request.GET.get('next') or request.POST.get('next') or reverse('stock_movement_list')

    if request.method == 'POST':

        if request.POST.get('delete_product') == '1':
            sm_obj.delete()

            # Bir hareket güncellendi ya da silindiğinde:
            recalculate_stock_quantity(sm_obj.product, sm_obj.warehouse)

            messages.success(request, "🗑️ Kayıt tamamen silindi.")
            return redirect(next_url)
        

        form = StockMovementForm(request.POST, instance=sm_obj)
        if form.is_valid():
            updated_movement = form.save(commit=False)

            # ✅ Her şey yolundaysa uygula
            with transaction.atomic():
                updated_movement.save()

                # Bir hareket güncellendi ya da silindiğinde:
                recalculate_stock_quantity(sm_obj.product, sm_obj.warehouse)

                messages.success(request, "Hareket ve stok başarıyla güncellendi.")
                return redirect(next_url)

    else:
        form = StockMovementForm(instance=sm_obj)

    return render(request, 'inventory/edit_stock_movement.html', {
        'form': form,
        'sm_obj': sm_obj
    })






@login_required
def expiring_products(request):
    today = date.today()
    three_months_later = today + timedelta(days=90)

    # Stokta kalan ve SKT'si 3 ay içinde olan ürünler
    expiring_stocks = (
        Stock.objects
        .filter(expiration_date__range=(today, three_months_later), quantity__gt=0)
        .select_related('product', 'warehouse')
        .order_by('expiration_date')
    )

    return render(request, 'inventory/expiring_products.html', {
        'expiring_stocks': expiring_stocks,
        'title': 'Son Kullanma Tarihi Yaklaşan Ürünler',
        'today': today
    })
    
    




@login_required
def temperature_alert_view(request):
    # Uygunsuz sıcaklıkta olan stoklar
    violating_stocks = Stock.objects.select_related('warehouse', 'product').filter(
        warehouse__temperature__lt=F('product__min_temperature')
    ) | Stock.objects.select_related('warehouse', 'product').filter(
        warehouse__temperature__gt=F('product__max_temperature')
    )

    return render(request, 'inventory/temperature_alert.html', {
        'violating_stocks': violating_stocks
    })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta

from .models import Product, Warehouse, Stock, StockMovement
from django.db.models import F


@login_required
def dashboard_view(request):
    today = date.today()
    warning_date = today + timedelta(days=30)

    distinct_product_count = Stock.objects.values('product').distinct().count()


    expiring_soon = Stock.objects.filter(expiration_date__lte=warning_date).count()



    # Uygunsuz sıcaklıkta olan stokları filtrele
    violating_stocks = Stock.objects.select_related('warehouse', 'product').filter(
        warehouse__temperature__lt=F('product__min_temperature')
    ) | Stock.objects.select_related('warehouse', 'product').filter(
        warehouse__temperature__gt=F('product__max_temperature')
    )
    high_temp_warehouses = violating_stocks.count()


    stocks = Stock.objects.select_related('product', 'warehouse')
    product_stock_map = defaultdict(int)  # {product_obj: total_quantity}

    # Stokları ürün bazında grupla ve topla
    for stock in stocks:
        product_stock_map[stock.product] += stock.quantity

    chart_labels = []
    chart_stocks = []
    chart_critical_levels = []
    critical_stocks = 0

    # Artık her ürün için işlem yapabiliriz
    for product, total_quantity in product_stock_map.items():
        chart_labels.append(product.name)
        chart_stocks.append(total_quantity)
        chart_critical_levels.append(product.critical_level)

        if total_quantity <= product.critical_level:
            critical_stocks += 1



    warehouse_chart_labels = []
    warehouse_chart_data = []

    warehouses = Warehouse.objects.all()
    stocks = Stock.objects.select_related('warehouse')

    for warehouse in warehouses:
        # O depoya ait tüm stokların toplam miktarı
        total_quantity = sum(
            stock.quantity for stock in stocks if stock.warehouse == warehouse
        )

        warehouse_chart_labels.append(warehouse.name)
        warehouse_chart_data.append(total_quantity)



    return render(request, 'inventory/dashboard.html', {
        'distinct_product_count': distinct_product_count,
        'critical_stocks': critical_stocks,
        'expiring_soon': expiring_soon,
        'high_temp_warehouses': high_temp_warehouses,
        'chart_labels': chart_labels,
        'chart_stocks': chart_stocks,
        'chart_critical_levels': chart_critical_levels,
        'warehouse_chart_labels': warehouse_chart_labels,
        'warehouse_chart_data': warehouse_chart_data
    })



@login_required
def export_all_stocks_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tum_stoklar.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 50, "📦 Tüm Stok Kayıtları")

    p.setFont("Helvetica", 11)
    y = height - 80

    stocks = Stock.objects.select_related('product', 'warehouse').order_by('product__name')

    for stock in stocks:
        text = f"{stock.product.name} - {stock.warehouse.name} | Miktar: {stock.quantity} | SKT: {stock.expiration_date.strftime('%d.%m.%Y')}"
        p.drawString(40, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 11)
            y = height - 50

    p.showPage()
    p.save()
    return response


@login_required
def forecast_stock(request, product_id):
    product = Product.objects.get(id=product_id)

    movements = (
        StockMovement.objects.filter(product=product, movement_type='OUT')
        .exclude(timestamp=None)
        .values('timestamp')
        .annotate(total=Sum('quantity'))
        .order_by('timestamp')
    )

    if not movements:
        return render(request, 'inventory/forecast.html', {'message': 'Veri yok'})

    df = pd.DataFrame(movements)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    ts = df['total'].asfreq('D', fill_value=0)
    if len(ts) < 3:
         return render(request, 'inventory/forecast.html', {
        'product': product,
        'message': 'Yeterli veri yok. En az 3 OUT hareketi gerekiyor.'
    })
    model = ExponentialSmoothing(ts, trend='add', seasonal=None).fit()
    forecast = model.forecast(7)

    plt.figure(figsize=(8, 4))
    ts.plot(label='Gerçek')
    forecast.plot(label='Tahmin', linestyle='--')
    plt.legend()
    plt.title(f"{product.name} - 7 Günlük Tüketim Tahmini")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render(request, 'inventory/forecast.html', {
        'product': product,
        'image': image_base64
    })


from django.utils.timezone import now

@login_required
def depletion_forecast_view(request):
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    today = now().date()

    forecast_data = []

    for product in products:
        total = 0
        for warehouse in warehouses:
            in_qty = StockMovement.objects.filter(
                product=product, warehouse=warehouse, movement_type='IN'
            ).aggregate(Sum('quantity'))['quantity__sum'] or 0

            out_movements = StockMovement.objects.filter(
                product=product, warehouse=warehouse, movement_type='OUT'
            ).order_by('timestamp')

            out_qty = out_movements.aggregate(Sum('quantity'))['quantity__sum'] or 0
            total += in_qty - out_qty

            if out_movements.exists():
                first_date = out_movements.first().timestamp.date()
                day_diff = (today - first_date).days or 1  # 0 olmasın

                daily_consumption = out_qty / day_diff
                days_remaining = int(total / daily_consumption) if daily_consumption > 0 else '∞'
            else:
                daily_consumption = 0
                days_remaining = '∞'

            forecast_data.append({
                'product': product,
                'warehouse': warehouse,
                'stock': total,
                'daily_consumption': round(daily_consumption, 2),
                'days_remaining': days_remaining,
            })

    return render(request, 'inventory/depletion_forecast.html', {
        'forecast_data': forecast_data
    })



    warehouses = Warehouse.objects.all()
    warehouse_labels = []
    warehouse_totals = []

    for warehouse in warehouses:
        total = StockMovement.objects.filter(
            warehouse=warehouse, movement_type='IN'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        total -= StockMovement.objects.filter(
            warehouse=warehouse, movement_type='OUT'
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0

        warehouse_labels.append(warehouse.name)
        warehouse_totals.append(total)
        
