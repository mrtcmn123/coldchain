from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Product, Warehouse
from inventory.forms import ProductForm, WarehouseForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def depo_yönetimi(request):
    warehouses = Warehouse.objects.all()
    form = WarehouseForm()


    return render(request, 'warehouse/depo_yönetimi.html', {
        'warehouses': warehouses,
        'form': form,
    })


@csrf_exempt
def update_temperatures(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data.get('temperatures', []):
                warehouse_id = item.get('id')
                new_temp = item.get('temperature')
                if warehouse_id and new_temp is not None:
                    Warehouse.objects.filter(id=warehouse_id).update(temperature=new_temp)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


@login_required
def warehouse_edit(request, obj_id):
    warehouse_obj = get_object_or_404(Warehouse, id=obj_id)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse_obj)

        if request.POST.get('delete_product') == '1':
            warehouse_obj.delete()
            messages.success(request, "🗑️ Depo tamamen silindi.")
            return redirect('depo_yönetimi')
        
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Depo başarıyla güncellendi.")
            return redirect('depo_yönetimi')
    else:
        form = WarehouseForm(instance=warehouse_obj)

    return render(request, 'warehouse/edit_warehouse.html', {
        'form': form
    })




@csrf_exempt
def create_warehouse_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            location = data.get('location')
            temperature = data.get('temperature')

            if not name or not location or temperature is None:
                return JsonResponse({'success': False, 'message': 'Tüm alanlar zorunludur.'})

            Warehouse.objects.create(
                name=name,
                location=location,
                temperature=temperature
            )
            return JsonResponse({'success': True, 'message': 'Depo başarıyla oluşturuldu.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Geçersiz JSON verisi.'})

    return JsonResponse({'success': False, 'message': 'Sadece POST istekleri desteklenir.'})