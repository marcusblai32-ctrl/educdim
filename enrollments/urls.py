from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.enrollment_list, name='list'),
    path('<int:pk>/', views.enrollment_detail, name='detail'),
    path('enroll/<int:cours_pk>/', views.enroll_course, name='enroll_course'),  # AJOUTE SA
    path('admin/pending/', views.admin_pending, name='admin_pending'),
    path('admin/approve/<int:pk>/', views.admin_approve_enrollment, name='admin_approve'),
    path('admin/reject/<int:pk>/', views.admin_reject_enrollment, name='admin_reject'),
]