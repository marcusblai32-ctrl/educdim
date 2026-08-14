from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Anciennes URLs
    path('', views.notification_list, name='list'),
    path('mark-read/<int:pk>/', views.mark_read_ajax, name='mark_read_ajax'),
    path('delete/<int:pk>/', views.delete_notification, name='delete'),
    path('delete-all/', views.delete_all_notifications, name='delete_all'),
    path('unread-count/', views.get_unread_count, name='unread_count'),

    # Nouvelles URLs
    path('enroll/free/<int:course_id>/', views.enroll_free_course, name='enroll_free_course'),
    path('admin/enrollments/<int:enrollment_id>/approve/', views.approve_enrollment, name='approve_enrollment'),
    path('admin/enrollments/<int:enrollment_id>/reject/', views.reject_enrollment, name='reject_enrollment'),
    path('admin/subscriptions/<int:subscription_id>/approve/', views.approve_subscription, name='approve_subscription'),
    path('subscriptions/<int:subscription_id>/confirm/', views.confirm_subscription, name='confirm_subscription'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('test/', views.test_notification, name='test'),
    path('test/email/', views.test_email, name='test_email'),
    path('test/sms/', views.test_sms, name='test_sms'),
]