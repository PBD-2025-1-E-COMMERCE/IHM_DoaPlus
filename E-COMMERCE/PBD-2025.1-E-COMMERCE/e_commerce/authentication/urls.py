from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('user/', views.user_page, name='user'),
    path('logout/', views.handle_logout, name='logout'),
    path('list_users/', views.list_users, name='list_users'),

]
