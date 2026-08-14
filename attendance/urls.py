from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.student_attendance, name='student_list'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('justifier/<int:fiche_pk>/', views.submit_justification, name='submit_justification'),
    path('reviser/<int:pk>/', views.review_justification, name='review_justification'),
]
