from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterItem, RegisterCompany
from .models import Company, Itens


def index(request):
    return render(request, 'index.html')


def item_dashboard(request):
    return render(request, 'item_dashboard.html')


@login_required
def dash(request):
    return render(request, 'dash.html')


def create_item(request):
    form = RegisterItem()
    if request.method == 'POST':
        form = RegisterItem(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:sales_dashboard')
    else:
        form = RegisterItem()
    context = {'form': form}
    return render(request, 'create_item.html', context)


def list_companies(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'list_companies.html', context)


def list_itens(request):
    itens = Itens.objects.all().order_by('name')
    context = {'itens': itens}
    return render(request, 'list_itens.html', context)


def create_company(request):
    form = RegisterCompany()
    if request.method == 'POST':
        form = RegisterCompany(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('authentication:login')
    else:
        form = RegisterCompany()
    context = {'form': form}
    return render(request, 'create_company.html', context)
