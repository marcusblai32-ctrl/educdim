from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.liste_salons, name='liste_salons'),
    path('salon/<int:pk>/', views.detail_salon, name='detail_salon'),
    path('message/<int:pk>/supprimer/', views.supprimer_message, name='supprimer_message'),
    path('etudiants/', views.liste_etudiants_chat, name='liste_etudiants'),
    path('prive/<int:user_id>/', views.creer_salon_prive, name='creer_prive'),
    path('groupe/<int:course_pk>/', views.creer_salon_groupe, name='creer_groupe'),
    path('feedback/<int:user_id>/', views.creer_salon_feedback, name='creer_feedback'),
    path('salon/<int:room_pk>/messages/<int:last_message_id>/',
         views.get_new_messages,
         name='get_new_messages'),
    path('salon/<int:room_pk>/send/',
         views.send_message,
         name='send_message'),
]
