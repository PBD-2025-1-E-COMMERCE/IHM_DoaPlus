from pyexpat.errors import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterItem, RegisterCompany
from .models import Company, Item, ItemDetails, Image, Category, User, Ongs, Causa, Cupom


def index(request):
    causas = Causa.objects.all().order_by('title')

    query = request.GET.get('q')
    user = request.user

    if query:
        causas = Causa.objects.filter(name__icontains=query)
        if not causas.exists():
            causas = Causa.objects.all().order_by('title')

    companies = Company.objects.all()
    for causa in causas:
        porcentagem = min((causa.valor_arrecadado / causa.value) * 100, 100)
        causa.porcentagem = porcentagem

    context = {

        'causas': causas,
        'companies': companies,
        'porcentagem': porcentagem
    }

    return render(request, 'index.html', context)


'''def index(request):
    itens = Item.objects.all().order_by('name')
    query = request.GET.get('q')
    user = request.user

    if query:
        itens = Item.objects.filter(name__icontains=query)
        if not itens.exists():
            itens = Item.objects.all().order_by('name')

    companies = Company.objects.all()

    context = {
        'itens': itens,
        'companies': companies,
    }

    return render(request, 'index.html', context)'''


@login_required
def dash(request):
    user = request.user

    return render(request, 'dash.html')


def create_campanha(request):
    """form = RegisterItem()
    if request.method == 'POST':
        form = RegisterItem(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ecommerce:sales_dashboard')
    else:
        form = RegisterItem()
    context = {'form': form}"""
    return render(request, 'create_campanha.html')


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
    companies = Company.objects.filter(logo=company.logo)
    itens = Item.objects.filter(company_id=company)

    query = request.GET.get('q')
    if query:
        itens = Item.objects.filter(company_id=company, name__icontains=query)
        if not itens.exists():
            itens = Item.objects.filter(company_id=company)

    context = {
        'company': company,
        'itens': itens,
        'companies': companies
    }
    return render(request, 'company_page.html', context)


def causa_dashboard(request, title):
    user = request.user
    query = request.GET.get('q')
    causa = get_object_or_404(Causa, title=title)

    if causa.value > 0:
        causa.porcentagem = min(
            (causa.valor_arrecadado / causa.value) * 100, 100)
    else:
        causa.porcentagem = 0

    if query:
        causas = Causa.objects.filter(name__icontains=query)
        if causas.count() >= 2:
            context = {'causas': causas}
            return render(request, 'index.html', context)
        elif causas.count() == 1:
            causa = causas.first()

    if request.method == "POST":
        valor_str = request.POST.get("valor")

        if not valor_str:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'sucesso': False, 'erro': 'Valor inválido'}, status=400)
            return redirect('ecommerce:causa_dashboard', title=causa.title)

        valor = float(valor_str)
        causa.valor_arrecadado += Decimal(str(valor))

        if request.user.is_authenticated:
            try:
                cupom_ganho = None

                if 50.00 <= valor < 100.00:
                    cupom_ganho = Cupom.objects.get(codigo="CUPOM10")
                elif 100.00 <= valor < 200.00:
                    cupom_ganho = Cupom.objects.get(codigo="CUPOM20")
                elif 200.00 <= valor < 500.00:
                    cupom_ganho = Cupom.objects.get(codigo="VOUCHER50")
                elif valor >= 500.00:
                    cupom_ganho = Cupom.objects.get(codigo="VOUCHER100")

                if cupom_ganho:
                    request.user.cupom.add(cupom_ganho)

            except Cupom.DoesNotExist:
                print("Cupom não encontrado no sistema.")

        if causa.value > 0:
            causa.porcentagem = min(
                (causa.valor_arrecadado / causa.value) * 100, 100)

        if causa.porcentagem >= 100:
            causa.ativo = False

        causa.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'sucesso': True,
                'url': reverse('ecommerce:causa_dashboard', args=[causa.title]),
                'cupom': cupom_ganho.codigo if cupom_ganho else None
            })

        return redirect('ecommerce:causa_dashboard', title=causa.title)

    context = {
        'causa': causa,
    }

    return render(request, 'causa_dashboard.html', context)


'''def item_dashboard(request):
    user = request.user
    query = request.GET.get('q')
    item = get_object_or_404(Item, code_item=id)
    details = ItemDetails.objects.filter(item=item)
    galery = Image.objects.filter(item=item)

    if query:
        itens = Item.objects.filter(name__icontains=query)
        if itens.count() >= 2:
            context = {'itens': itens}
            return render(request, 'index.html', context)
        elif itens.count() == 1:    
            item = itens.first()
            details = ItemDetails.objects.filter(item=item)
            galery = Image.objects.filter(item=item)

    context = {
        'item': item,
        'galery': galery,
        'details': details,
    }
    return render(request, 'item_dashboard.html')'''


def category_page(request, category):
    categoria = get_object_or_404(Category, id=category)
    item = Item.objects.filter(category=categoria)
    ongs = Ongs.objects.all().order_by('name')
    companies = Company.objects.all()
    query = request.GET.get('q')
    if query:
        item = Item.objects.filter(category=categoria, name__icontains=query)
        if not item.exists():
            item = Item.objects.filter(category=categoria)

    context = {
        'item': item,
        'companies': companies,
        'categoria': categoria,
        'ong': ongs
    }

    return render(request, 'category_page.html', context)


def companies(request):
    companies = Company.objects.all()
    query = request.GET.get('q')
    if query:
        companies = Company.objects.filter(name__icontains=query)
    else:
        companies = Company.objects.all().order_by('name')
    context = {'companies': companies}
    return render(request, 'companies.html', context)


def home(request):
    return render(request, "home.html")


def meus_cupons(request):
    return render(request, 'list_cupons.html')
