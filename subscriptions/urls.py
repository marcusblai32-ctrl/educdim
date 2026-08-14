from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.subscription_list, name='list'),
    path('abonner/<int:plan_pk>/', views.subscribe, name='subscribe'),
    path('mes-abonnements/', views.my_subscriptions, name='my_subscriptions'),
    path('mon-abonnement/<int:pk>/', views.subscription_detail, name='detail'),
    path('admin/en-attente/', views.admin_pending, name='admin_pending'),
]
