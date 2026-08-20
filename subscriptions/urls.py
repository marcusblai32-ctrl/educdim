from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # URLs ki deja egziste
    path('', views.subscription_list, name='list'),
    path('souscrire/<int:plan_pk>/', views.subscribe, name='subscribe'),
    path('mes-abonnements/', views.my_subscriptions, name='my_subscriptions'),
    path('detail/<int:pk>/', views.subscription_detail, name='detail'),
    path('admin/en-attente/', views.admin_pending, name='admin_pending'),
    path('admin/verifier/<int:pk>/', views.admin_verify_subscription, name='admin_verify'),
    
    # ===== NOUVO URLs =====
    path('chwazi-kou/<int:pk>/', views.select_courses, name='select_courses'),
]