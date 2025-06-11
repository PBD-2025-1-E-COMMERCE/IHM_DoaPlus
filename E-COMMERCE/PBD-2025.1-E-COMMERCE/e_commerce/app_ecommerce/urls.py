from django.contrib import admin
from django.urls import path
from app_ecommerce import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.index, name='index'),

    path('item_dashboard/', views.item_dashboard, name='item_dashboard'),
    path('dash/', views.dash, name='dash'),

    path('create_item/', views.create_item, name='create_item'),
    path('list_itens/', views.list_itens, name='list_itens'),


    path('create_company/', views.create_company, name='create_company'),
    path('list_companies/', views.list_companies, name='list_companies'),


]
