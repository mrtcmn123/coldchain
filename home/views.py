from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Product
from inventory.forms import ProductForm

# Create your views here.
@login_required
def ayarlar(request):
    
    return render(request, 'home/ayarlar.html', {
    })