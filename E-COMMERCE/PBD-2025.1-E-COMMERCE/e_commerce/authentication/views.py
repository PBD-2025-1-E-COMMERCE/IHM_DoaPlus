from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render
from .forms import UserLoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.decorators import login_required


def user_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # salva sem ainda salvar no banco
            # ou 'password' dependendo do form
            password = form.cleaned_data.get('password')
            user.set_password(password)  # agora sim, senha criptografada!
            user.save()
            messages.success(request, "Usuário registrado com sucesso!")
            return redirect('ecommerce:index')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'create_user.html', context)


def login_page(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if User.is_admin==True and user:
                login(request, user=user)
                return redirect('ecommerce:dash')
            elif user:
                login(request, user=user)
                return redirect('ecommerce:index')
    context = {'form': form}
    return render(request, 'login.html', context)


def handle_logout(request):
    logout(request)
    return redirect('authentication:login')


@login_required
def list_users(request):
    users = User.objects.all()
    contex = {'users': users}
    return render(request, 'list_users.html', contex)
