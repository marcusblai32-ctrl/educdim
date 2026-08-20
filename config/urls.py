from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from courses.views import about_page, contact_page, conditions_page, privacy_page, faq_page


admin.site.site_header = "Administration EducDim"
admin.site.site_title = "Administration EducDim"
admin.site.index_title = "Bienvenue dans l'administration EducDim"


urlpatterns = [
    path('dp/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('cours/', include('courses.urls')),
    path('inscriptions/', include('enrollments.urls')),
    path('abonnements/', include('subscriptions.urls')),
    path('progression/', include('progress.urls')),
    path('quiz/', include('quiz.urls')),
    path('presence/', include('attendance.urls')),
    path('badges/', include('badges.urls')),
    path('classement/', include('ranking.urls')),
    path('chat/', include('chat.urls')),
    path('notifications/', include('notifications.urls')),
    path('theme/', include('theme_manager.urls')),
    path('ads/', include('ads.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('a-propos/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('conditions/', conditions_page, name='conditions'),
    path('confidentialite/', privacy_page, name='privacy'),
    path('faq/', faq_page, name='faq'),

    # ===== CHANJMAN: TRUE olye FALSE =====
    prefix_default_language=True,
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)