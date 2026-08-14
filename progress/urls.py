from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cours/<int:pk>/', views.course_progress, name='course_progress'),
    path('lecon/<int:lecon_pk>/terminer/', views.mark_lecon_complete, name='mark_lecon_complete'),
]
