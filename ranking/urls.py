from django.urls import path
from . import views

app_name = 'ranking'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('mon-rang/', views.my_rank, name='my_rank'),
]
