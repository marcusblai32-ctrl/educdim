from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from courses.views import about_page, contact_page, conditions_page, privacy_page, faq_page

# ============================================
# URL SANS PREFIX LANG (admin, i18n, redireksyon)
# ============================================
urlpatterns = [
    path('dp/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    
    # ===== REDIREKSYON POU ANSYEN URLs SAN PREFIKS =====
    path('accounts', lambda request: redirect('/fr/accounts/', permanent=True)),
    path('accounts/', lambda request: redirect('/fr/accounts/', permanent=True)),
    path('cours', lambda request: redirect('/fr/cours/', permanent=True)),
    path('cours/', lambda request: redirect('/fr/cours/', permanent=True)),
    path('abonnements', lambda request: redirect('/fr/abonnements/', permanent=True)),
    path('abonnements/', lambda request: redirect('/fr/abonnements/', permanent=True)),
    path('quiz', lambda request: redirect('/fr/quiz/', permanent=True)),
    path('quiz/', lambda request: redirect('/fr/quiz/', permanent=True)),
    path('chat', lambda request: redirect('/fr/chat/', permanent=True)),
    path('chat/', lambda request: redirect('/fr/chat/', permanent=True)),
    path('badges', lambda request: redirect('/fr/badges/', permanent=True)),
    path('badges/', lambda request: redirect('/fr/badges/', permanent=True)),
    path('classement', lambda request: redirect('/fr/classement/', permanent=True)),
    path('classement/', lambda request: redirect('/fr/classement/', permanent=True)),
    path('notifications', lambda request: redirect('/fr/notifications/', permanent=True)),
    path('notifications/', lambda request: redirect('/fr/notifications/', permanent=True)),
    path('progression', lambda request: redirect('/fr/progression/', permanent=True)),
    path('progression/', lambda request: redirect('/fr/progression/', permanent=True)),
]

# ============================================
# URL AVEC PREFIX LANG (fr/ ak ht/)
# ============================================
urlpatterns += i18n_patterns(
    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Courses
    path('cours/', include('courses.urls')),

    # Enrollments
    path('inscriptions/', include('enrollments.urls')),

    # Subscriptions
    path('abonnements/', include('subscriptions.urls')),

    # Progress
    path('progression/', include('progress.urls')),

    # Quiz
    path('quiz/', include('quiz.urls')),

    # Attendance
    path('presence/', include('attendance.urls')),

    # Badges
    path('badges/', include('badges.urls')),

    # Ranking
    path('classement/', include('ranking.urls')),

    # Chat
    path('chat/', include('chat.urls')),

    # Notifications
    path('notifications/', include('notifications.urls')),

    # Theme Manager
    path('theme/', include('theme_manager.urls')),

    # Ads
    path('ads/', include('ads.urls')),

    # Dashboard
    path('dashboard/', include('dashboard.urls')),

    # Pages statiques
    path('a-propos/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('conditions/', conditions_page, name='conditions'),
    path('confidentialite/', privacy_page, name='privacy'),
    path('faq/', faq_page, name='faq'),

    # ===== CHANJMAN: Mete False pou TOU DE lang yo gen prefiks =====
    prefix_default_language=False,
)

# ============================================
# STATIC & MEDIA FILES (DEBUG SEULEMENT)
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)