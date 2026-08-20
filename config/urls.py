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

    # ===== Mete True pou lang default pa gen prefiks =====
    prefix_default_language=True,
)

# ============================================
# REDIRECTIONS POUR ANSIENNES URLS
# ============================================
urlpatterns += [
    # Redireksyone /fr/ sou / (lang default)
    path('fr/', lambda request: redirect('/', permanent=False)),
    
    # Redireksyone ansyen URLs san prefiks
    path('accounts', lambda request: redirect('/accounts/', permanent=True)),
    path('accounts/', lambda request: redirect('/accounts/', permanent=True)),
    path('cours', lambda request: redirect('/cours/', permanent=True)),
    path('cours/', lambda request: redirect('/cours/', permanent=True)),
    path('abonnements', lambda request: redirect('/abonnements/', permanent=True)),
    path('abonnements/', lambda request: redirect('/abonnements/', permanent=True)),
]

# ============================================
# STATIC & MEDIA
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)