from django.db import models

class Banner(models.Model):
    PLACEMENTS = [
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
    ]
    titre = models.CharField(max_length=200, verbose_name="Titre")
    image = models.ImageField(upload_to='banners/', verbose_name="Image")
    lien = models.URLField(blank=True, verbose_name="Lien")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    largeur = models.PositiveIntegerField(default=1200, verbose_name="Largeur (px)")
    hauteur = models.PositiveIntegerField(default=400, verbose_name="Hauteur (px)")
    placement = models.CharField(max_length=10, choices=PLACEMENTS, default='header', verbose_name="Placement")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Bannière"
        verbose_name_plural = "Bannières"

    def __str__(self):
        return self.titre
