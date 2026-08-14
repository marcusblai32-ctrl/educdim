from django.urls import path
from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.badge_list, name='list'),
    path('mes-badges/', views.my_badges, name='my_badges'),
    path('<int:pk>/', views.badge_detail, name='detail'),
]
