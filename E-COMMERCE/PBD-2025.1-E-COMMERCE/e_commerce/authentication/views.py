from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User


def user_page(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect('ecommerce:index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    contex = {'form': form}
    return render(request, 'create_user.html', contex)


def login_page(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user=user)
                return redirect('ecommerce:dash')
    context = {'form': form}
    return render(request, 'login.html', context)


def handle_logout(request):
    logout(request)
    return redirect('authentication:login')


def list_users(request):
    users = User.objects.all()
    contex = {'users': users}
    return render (request, 'list_users.html', contex)
