from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # Todo List
    path('', views.todo_list, name='todo_list'),
    path('create/', views.create_todo, name='create_todo'),
    path('<int:pk>/edit/', views.update_todo, name='update_todo'),
    path('<int:pk>/delete/', views.delete_todo, name='delete_todo'),
    path('<int:pk>/toggle/', views.toggle_todo_status, name='toggle_todo'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    
    # Export/Local Storage
    path('export/json/', views.export_todos_json, name='export_json'),
]
