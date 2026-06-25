from .models import Causa, Cupom  # Ajuste os seus imports conforme necessário
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterItem, RegisterCompany, RegisterCausa
from .models import Company, Item, ItemDetails, Image, Category, User, Ongs, Causa, Cupom


def index(request):
    query = request.GET.get('q')

    if query:

        causa_encontrada = Causa.objects.filter(
            title__icontains=query, ativo=True).first()

        categoria_id = 1

        if causa_encontrada:
            if causa_encontrada.ong:
                categoria_id = 2
            elif causa_encontrada.creator:
                categoria_id = 1

        url_redirecionamento = reverse('ecommerce:category_page', kwargs={
                                       'category': categoria_id})
        return redirect(f"{url_redirecionamento}?q={query}")

    causas = Causa.objects.all().order_by('title')
    companies = Company.objects.all()

    for causa in causas:
        if causa.value > 0:
            porcentagem = min(
                (causa.valor_arrecadado / causa.value) * 100, 100)
        else:
            porcentagem = 0
        causa.porcentagem = porcentagem

    context = {
        'causas': causas,
        'companies': companies,
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


@login_required
def create_campanha(request):
    query = request.GET.get('q')

    if query:
        query = query.strip()

        causas = Causa.objects.filter(title__icontains=query)

        return render(request, 'index.html', {'causas': causas, 'query': query})

    if request.method == 'POST':
        form = RegisterCausa(request.POST, request.FILES)

        if form.is_valid():
            causa = form.save(commit=False)
            causa.creator = request.user
            causa.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'sucesso': True}, status=201)

            return redirect('ecommerce:create_campanha')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'sucesso': False, 'erros': form.errors}, status=400)

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


@login_required
def minhas_campanhas(request):
    query = request.GET.get('q')

    if query:
        query = query.strip()

        causas = Causa.objects.filter(
            creator=request.user, title__icontains=query)
        return render(request, 'index.html', {'causas': causas, 'query': query})

    causas = Causa.objects.filter(creator=request.user).order_by('-id')

    context = {
        'causas': causas,
    }
    return render(request, 'minhas_campanhas.html', context)


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

    # 1. TRATAMENTO DA BARRA DE PESQUISA (Executado antes de carregar o resto da página)
    if query:
        query = query.strip()
        # CORREÇÃO: Mudado de 'name__icontains' para 'title__icontains'
        causas = Causa.objects.filter(title__icontains=query)

        if causas.count() >= 2:
            context = {'causas': causas}
            return render(request, 'index.html', context)

        elif causas.count() == 1:
            # CORREÇÃO: Faz o redirect real para atualizar a URL com o título novo
            causa_encontrada = causas.first()
            return redirect('ecommerce:causa_dashboard', title=causa_encontrada.title)

        else:
            # CORREÇÃO: Se não achou nenhuma, joga para o index renderizar o estado vazio
            return render(request, 'index.html', {'causas': causas, 'query': query})

    # 2. FLUXO NORMAL DO GET (Caso não haja busca)
    causa = get_object_or_404(Causa, title=title)

    if causa.value > 0:
        causa.porcentagem = min(
            (causa.valor_arrecadado / causa.value) * 100, 100)
    else:
        causa.porcentagem = 0

    # 3. TRATAMENTO DO DO POST (Doação/Apoio à causa)
    if request.method == "POST":
        valor_str = request.POST.get("valor")

        if not valor_str:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'sucesso': False, 'erro': 'Valor inválido'}, status=400)
            return redirect('ecommerce:causa_dashboard', title=causa.title)

        valor = float(valor_str)
        causa.valor_arrecadado += Decimal(str(valor))

        cupom_ganho = None
        if request.user.is_authenticated:
            try:
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


def item_dashboard(request, id):
    user = request.user
    query = request.GET.get('q')
    item = get_object_or_404(Item, code_item=id)
    details = ItemDetails.objects.filter(item=item)
    galery = Image.objects.filter(item=item)

    if query:
        itens = Item.objects.filter(name__icontains=query)
        if itens.count() >= 2:
            return render(request, 'index.html', {'itens': itens})
        elif itens.count() == 1:
            item = itens.first()
            details = ItemDetails.objects.filter(item=item)
            galery = Image.objects.filter(item=item)

    cupons_validos = []
    if user.is_authenticated:
        # Buscamos apenas os cupons vinculados a ele que estão na validade
        cupons_validos = user.cupom.filter(validade__gte=timezone.now())

    if request.method == 'POST':
        cupom_id = request.POST.get('cupom_id')
        variacao_id = request.POST.get('variacao_id')

        valor_final = item.price

        if cupom_id and cupom_id != "0":
            # Captura o cupom associado ao usuário
            cupom = get_object_or_404(user.cupom, id=cupom_id)

            if cupom.tipo_desconto == 'PERC':
                valor_final = item.price - \
                    (item.price * (cupom.desconto / 100))
            elif cupom.tipo_desconto == 'FIXO':
                valor_final = item.price - cupom.desconto

            if valor_final < 0:
                valor_final = 0

            user.cupom.remove(cupom)

            messages.success(
                request, f"Compra realizada com sucesso! Cupom {cupom.codigo} aplicado e removido da sua carteira. Valor final: R$ {valor_final:.2f}"
            )
        else:
            messages.success(
                request, f"Compra realizada com sucesso! Valor final: R$ {valor_final:.2f}"
            )

        return redirect('ecommerce:item_dashboard', id=item.code_item)

    context = {
        'item': item,
        'galery': galery,
        'details': details,
        'cupons': cupons_validos,
    }
    return render(request, 'item_dashboard.html', context)


def category_page(request, category):

    categoria = get_object_or_404(Category, id=category)

    query = request.GET.get('q')

    causas = None
    if categoria.id == 1:

        causas = Causa.objects.filter(creator__isnull=False, ativo=True)

        if query:
            causas = causas.filter(title__icontains=query)

    elif categoria.id == 2:

        causas = Causa.objects.filter(ong__isnull=False, ativo=True)

        if query:
            causas = causas.filter(title__icontains=query)

    item = Item.objects.filter(category=categoria)
    if query and categoria.id not in [1, 2]:
        item = Item.objects.filter(category=categoria, name__icontains=query)
        if not item.exists():
            item = Item.objects.filter(category=categoria)

    ongs = Ongs.objects.all().order_by('name')
    companies = Company.objects.all()

    context = {
        'item': item,
        'companies': companies,
        'categoria': categoria,
        'ong': ongs,
        'causas': causas,
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
