from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import UserLoginForm
from django.contrib.auth.signals import user_logged_out
from django.views.generic.base import TemplateView


@login_required
def home(request):
    return render(request, 'home.html')


def login_page(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request, user=user)
                return redirect('home')
    context = {'form': form}
    return render(request, 'login.html', context)


def logout(request):
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None

    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()

    if hasattr(request, "user"):
        request.user = User()

    return redirect('login')