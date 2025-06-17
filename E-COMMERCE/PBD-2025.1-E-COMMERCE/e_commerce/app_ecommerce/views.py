from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterItem, RegisterCompany
from .models import Company, Item


def index(request):
    companies = Company.objects.all()
    itens = Item.objects.all().order_by('name')
    context = {
        'itens': itens,
        'companies': companies
    }

    return render(request, 'index.html', context)


def item_dashboard(request):
    itens = Item.objects.all().order_by('name')
    context = {'itens': itens}
    return render(request, 'item_dashboard.html', context)


@login_required
def dash(request):
    user = request.user
    return render(request, 'dash.html')


@login_required
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


@login_required
def list_companies(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'list_companies.html', context)


@login_required
def list_itens(request):
    user = request.user
    company = user.company
    itens = Item.objects.filter(company_id=user.company)
    context = {'itens': itens}
    return render(request, 'list_itens.html', context)


@login_required
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
