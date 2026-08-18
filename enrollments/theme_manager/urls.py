from django.urls import path
from . import views

app_name = 'theme_manager'

urlpatterns = [
    path('css/', views.dynamic_css, name='dynamic_css'),
    path('preview/', views.theme_preview, name='preview'),
    
    # ===== URL POU IMAJ YO =====
    path('logo/', views.theme_logo, name='theme_logo'),
    path('favicon/', views.theme_favicon, name='theme_favicon'),
    path('hero-image/', views.theme_hero_image, name='theme_hero_image'),
    path('about-image/', views.theme_about_image, name='theme_about_image'),
    path('evenement-banner/', views.theme_evenement_banner, name='theme_evenement_banner'),
    path('evenement-logo/', views.theme_evenement_logo, name='theme_evenement_logo'),
]
