from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.enrollment_list, name='list'),
    path('<int:pk>/', views.enrollment_detail, name='detail'),
    path('inscrire/<int:cours_pk>/', views.enroll_course, name='enroll'),
    path('admin/en-attente/', views.admin_pending, name='admin_pending'),
    path('admin/approuver/<int:pk>/', views.admin_approve_enrollment, name='admin_approve'),
    path('admin/refuser/<int:pk>/', views.admin_reject_enrollment, name='admin_reject'),
]
