from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterItem, RegisterCompany
from .models import Company, Item, ItemDetails, Image, Category, User


def index(request):
    query = request.GET.get('q')  

    if query:
        itens = Item.objects.filter(name__icontains=query)
    else:
        itens = Item.objects.all().order_by('name')

    companies = Company.objects.all()

    context = {
        'itens': itens,
        'companies': companies,
    }

    return render(request, 'index.html', context)


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
    if user.is_admin:
        itens = Item.objects.all()
    else:
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


def company_page(request, id):
    company = get_object_or_404(Company, id_company=id)
    itens = Item.objects.filter(company_id=company)
    companies = Company.objects.filter(logo=company.logo)
    context = {
        'company': company,
        'itens': itens,
        'companies': companies
    }
    return render(request, 'company_page.html', context)


def item_dashboard(request, id):
    item = get_object_or_404(Item, code_item=id)
    details = ItemDetails.objects.filter(item=item)
    galery = Image.objects.filter(item=item)

    context = {
        'item': item,
        'galery': galery,
        'details': details,
    }
    return render(request, 'item_dashboard.html', context)


def category_page(request, category):
    categoria = get_object_or_404(Category, id=category)
    item = Item.objects.filter(category=categoria)
    companies = Company.objects.all()
    context = {
        'item': item,
        'companies': companies,
        'categoria': categoria
    }

    return render(request, 'category_page.html', context)


def companies(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'companies.html', context)

