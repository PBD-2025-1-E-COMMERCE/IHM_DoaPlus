from django.contrib import admin
from django.urls import path
from app_ecommerce import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.index, name='index'),


    path('dash/home', views.home, name='home'),

    path('create_campanha/', views.create_campanha, name='create_campanha'),
    path('list_itens/', views.list_itens, name='list_itens'),
    path('dash/list_itens/', views.list_itens, name='list_itens'),
    path('item/<int:id>', views.item_dashboard, name='item_dashboard'),

    path('create_company/', views.create_company, name='create_company'),
    path('dash/list_companies/', views.list_companies, name='list_companies'),
    path('companiespage/', views.companies, name='companies'),
    path('minhas_campanhas/', views.minhas_campanhas, name='minhas_campanhas'),

    path('empresa/<str:id>/', views.company_page, name='company_page'),
    path('causa/<str:title>', views.causa_dashboard, name='causa_dashboard'),
    path('item/categoria/<int:category>/',
         views.category_page, name='category_page'),

    path('meuscupons/', views.meus_cupons, name='meus_cupons')



]
