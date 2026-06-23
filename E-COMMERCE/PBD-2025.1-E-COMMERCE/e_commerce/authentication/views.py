from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.decorators import login_required


def user_page(request):
    if request.method == 'GET':
        user = User.objects.all()
        return render(request, 'create_user.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = User(
            email=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password,
        )

        user.set_password(password)
        user.save()
        return redirect('authentication:login')


def login_page(request):
    form = UserLoginForm()
    user = request.user
    if request.method == 'GET':
        if user.is_authenticated :
            return redirect('ecommerce:index') 
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user=user)
                return redirect('ecommerce:index')
    context = {'form': form}
    return render(request, 'login.html', context)


def handle_logout(request):
    logout(request)
    return redirect('ecommerce:index')


@login_required
def list_users(request):
    user = request.user
    company = user.company
    if user.is_admin:
        users = User.objects.all()
    else:
        users = User.objects.filter(company_id=user.company)
    contex = {'users': users}
    return render(request, 'list_users.html', contex)
