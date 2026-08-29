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
        return Course.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Si modèl la gen get_absolute_url, itilize l
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        return f"/cours/{obj.slug}/"