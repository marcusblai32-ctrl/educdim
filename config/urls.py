from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from courses.views import about_page, contact_page, conditions_page, privacy_page, faq_page


# ============================================
# PERSONNALISATION DE L'ADMINISTRATION
# ============================================
admin.site.site_header = "Administration EducDim"
admin.site.site_title = "Administration EducDim"
admin.site.index_title = "Bienvenue dans l'administration EducDim"


# ============================================
# URL SANS PRÉFIXE DE LANGUE
# ============================================
urlpatterns = [
    path('dp/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]


# ============================================
# URL AVEC PRÉFIXE DE LANGUE (fr/ et ht/)
# ============================================
urlpatterns += i18n_patterns(
    # Accueil
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Comptes utilisateurs
    path('accounts/', include('accounts.urls')),

    # Cours
    path('cours/', include('courses.urls')),

    # Inscriptions
    path('inscriptions/', include('enrollments.urls')),

    # Abonnements
    path('abonnements/', include('subscriptions.urls')),

    # Progression
    path('progression/', include('progress.urls')),

    # Quiz
    path('quiz/', include('quiz.urls')),

    # Présences
    path('presence/', include('attendance.urls')),

    # Badges
    path('badges/', include('badges.urls')),

    # Classement
    path('classement/', include('ranking.urls')),

    # Chat
    path('chat/', include('chat.urls')),

    # Notifications
    path('notifications/', include('notifications.urls')),

    # Gestionnaire de thème
    path('theme/', include('theme_manager.urls')),

    # Annonces publicitaires
    path('ads/', include('ads.urls')),

    # Tableau de bord
    path('dashboard/', include('dashboard.urls')),

    # Pages statiques
    path('a-propos/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('conditions/', conditions_page, name='conditions'),
    path('confidentialite/', privacy_page, name='privacy'),
    path('faq/', faq_page, name='faq'),

    # ===== TOU DE lang yo gen prefiks =====
    prefix_default_language=False,
)


# ============================================
# REDIRECTIONS — Mete APRÈ i18n_patterns
# Sa ap sèlman mache si URL la pa deja matche
# ============================================
urlpatterns += [
    # Redireksyone rasin sou /fr/
    path('', lambda request: redirect('/fr/', permanent=False)),
    
    # Redireksyone ansyen URLs san prefiks
    path('accounts/', lambda request: redirect('/fr/accounts/', permanent=True)),
    path('cours/', lambda request: redirect('/fr/cours/', permanent=True)),
    path('abonnements/', lambda request: redirect('/fr/abonnements/', permanent=True)),
    path('quiz/', lambda request: redirect('/fr/quiz/', permanent=True)),
    path('chat/', lambda request: redirect('/fr/chat/', permanent=True)),
    path('badges/', lambda request: redirect('/fr/badges/', permanent=True)),
    path('classement/', lambda request: redirect('/fr/classement/', permanent=True)),
    path('notifications/', lambda request: redirect('/fr/notifications/', permanent=True)),
    path('progression/', lambda request: redirect('/fr/progression/', permanent=True)),
    path('presence/', lambda request: redirect('/fr/presence/', permanent=True)),
    path('inscriptions/', lambda request: redirect('/fr/inscriptions/', permanent=True)),
]

# ============================================
# STATIC & MEDIA
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)