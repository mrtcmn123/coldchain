from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # veya gideceği sayfa
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("login")
