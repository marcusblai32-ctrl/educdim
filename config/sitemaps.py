from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from courses.models import Course


class StaticViewSitemap(Sitemap):
    """Sitemap pou paj statik yo"""
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'conditions',
            'privacy',
            'faq',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


class CourseSitemap(Sitemap):
    """Sitemap pou kous yo"""
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Sèvi ak 'publie' — menm jan ak course_list view la
        return Course.objects.filter(publie=True)

    def lastmod(self, obj):
        # Tcheke si 'date_modification' egziste, sinon itilize 'date_creation'
        if hasattr(obj, 'date_modification'):
            return obj.date_modification
        elif hasattr(obj, 'date_creation'):
            return obj.date_creation
        else:
            return timezone.now()

    def location(self, obj):
        # Sèvi ak URL named pattern avèk pk (menm jan ak course_detail view la)
        return reverse('courses:course_detail', args=[obj.pk])