from django.urls import path
from . import views

app_name = 'theme_manager'

urlpatterns = [
    path('css/', views.dynamic_css, name='dynamic_css'),
    path('preview/', views.theme_preview, name='preview'),
]
