from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('ajouter/', views.course_create, name='course_add'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/modifier/', views.course_update, name='course_edit'),
    path('<int:pk>/supprimer/', views.course_delete, name='course_delete'),
    path('<int:pk>/toggle-inscription/', views.toggle_inscription, name='toggle_inscription'),

    # Learning Path (NOUVEAU)
    path('learning-paths/', views.learning_path_list, name='learning_path_list'),
    path('learning-paths/<int:pk>/', views.learning_path_detail, name='learning_path_detail'),

    # Structure du cours (EXISTANT)
    path('unite/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('lecon/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),
]