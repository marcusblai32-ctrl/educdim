from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, default="fas fa-tag", verbose_name="Icône FontAwesome")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

class Niveau(models.Model):
    NIVEAUX = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    nom = models.CharField(max_length=20, choices=NIVEAUX, default='debutant', verbose_name="Niveau")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"

    def __str__(self):
        return self.get_nom_display()

class Promotions(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la promotion")
    nivo = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Niveau")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(verbose_name="Date de fin")
    cours = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions', verbose_name="Cours associé")
    etudiants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='promotions', verbose_name="Étudiants")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.nom} ({self.date_debut|date:'d/m/Y'})"

    def nombre_etudiants(self):
        return self.etudiants.count()

class Course(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image_url = models.URLField(blank=True, verbose_name="URL de l'image (recommandée)")
    image = models.ImageField(upload_to='cours/images/', blank=True, null=True, verbose_name="Image (téléchargée)")
    prix = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="Prix (0 = gratuit)")
    publie = models.BooleanField(default=False, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='cours_crees', verbose_name="Créé par")

    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours', verbose_name="Catégorie")
    nivo = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours', verbose_name="Niveau")
    duree = models.PositiveIntegerField(default=0, help_text="Durée en heures", verbose_name="Durée (heures)")
    date_debut_inscription = models.DateTimeField(null=True, blank=True, verbose_name="Début des inscriptions")
    date_fin_inscription = models.DateTimeField(null=True, blank=True, verbose_name="Fin des inscriptions")
    inscription_ouverte = models.BooleanField(default=True, verbose_name="Inscriptions ouvertes")
    promotion = models.ForeignKey(Promotions, on_delete=models.SET_NULL, null=True, blank=True, related_name='cours_promo', verbose_name="Promotion")

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['titre']

    @property
    def est_payant(self):
        return self.prix > 0

    @property
    def inscription_possible(self):
        if not self.inscription_ouverte:
            return False
        if self.date_debut_inscription and self.date_fin_inscription:
            from django.utils import timezone
            now = timezone.now()
            return self.date_debut_inscription <= now <= self.date_fin_inscription
        return True

    def __str__(self):
        return self.titre

    def get_image(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return None

class Unite(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='unites', verbose_name="Cours")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Unité"
        verbose_name_plural = "Unités"
        ordering = ['cours', 'ordre']

    def __str__(self):
        return f"{self.cours.titre} - Unité {self.ordre}: {self.titre}"

class Module(models.Model):
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE, related_name='modules', verbose_name="Unité")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['unite', 'ordre']

    def __str__(self):
        return f"{self.unite} - Module {self.ordre}: {self.titre}"

class Lecon(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lecons', verbose_name="Module")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    contenu = models.TextField(blank=True, verbose_name="Contenu texte")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Quiz associé")

    class Meta:
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"
        ordering = ['module', 'ordre']

    def __str__(self):
        return f"{self.module} - Leçon {self.ordre}: {self.titre}"

class SectionLecon(models.Model):
    TYPES_SECTION = [
        ('introduction', 'Introduction'),
        ('developpement', 'Développement'),
        ('resume', 'Résumé'),
        ('exemple', 'Exemple'),
        ('exercice', 'Exercice'),
        ('autre', 'Autre'),
    ]
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE, related_name='sections', verbose_name="Leçon")
    titre = models.CharField(max_length=255, verbose_name="Titre")
    type_section = models.CharField(max_length=20, choices=TYPES_SECTION, default='developpement', verbose_name="Type")
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")

    class Meta:
        verbose_name = "Section de leçon"
        verbose_name_plural = "Sections de leçon"
        ordering = ['lecon', 'ordre']

    def __str__(self):
        return f"{self.lecon} - {self.titre}"

class Contenu(models.Model):
    TYPES_CONTENU = [
        ('texte', 'Texte'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('fichier', 'Fichier'),
        ('lien', 'Lien'),
    ]
    section = models.ForeignKey(SectionLecon, on_delete=models.CASCADE, related_name='contenus', verbose_name="Section")
    type_contenu = models.CharField(max_length=10, choices=TYPES_CONTENU, verbose_name="Type")
    titre = models.CharField(max_length=255, blank=True, verbose_name="Titre (FR)")
    texte = models.TextField(blank=True, verbose_name="Texte (FR)")
    url_video = models.URLField(blank=True, verbose_name="URL vidéo (FR)")
    url_image = models.URLField(blank=True, verbose_name="URL image (FR)")
    url_audio = models.URLField(blank=True, verbose_name="URL audio (FR)")
    url_pdf = models.URLField(blank=True, verbose_name="URL PDF (FR)")
    url_lien = models.URLField(blank=True, verbose_name="Lien externe (FR)")
    titre_ht = models.CharField(max_length=255, blank=True, verbose_name="Titre (HT)")
    texte_ht = models.TextField(blank=True, verbose_name="Texte (HT)")
    url_video_ht = models.URLField(blank=True, verbose_name="URL vidéo (HT)")
    url_image_ht = models.URLField(blank=True, verbose_name="URL image (HT)")
    url_audio_ht = models.URLField(blank=True, verbose_name="URL audio (HT)")
    url_pdf_ht = models.URLField(blank=True, verbose_name="URL PDF (HT)")
    url_lien_ht = models.URLField(blank=True, verbose_name="Lien externe (HT)")
    fichier_audio = models.FileField(upload_to='contenus/audio/', blank=True, null=True)
    image = models.ImageField(upload_to='contenus/images/', blank=True, null=True)
    fichier_pdf = models.FileField(upload_to='contenus/pdf/', blank=True, null=True)
    fichier = models.FileField(upload_to='contenus/fichiers/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=1, verbose_name="Ordre")

    class Meta:
        verbose_name = "Contenu"
        verbose_name_plural = "Contenus"
        ordering = ['section', 'ordre']

    def __str__(self):
        return f"{self.section} - {self.get_type_contenu_display()}: {self.titre or self.titre_ht or 'Sans titre'}"

    def get_titre(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.titre_ht:
            return self.titre_ht
        return self.titre

    def get_texte(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.texte_ht:
            return self.texte_ht
        return self.texte

    def get_video_url(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.url_video_ht:
            return self.url_video_ht
        return self.url_video

    def get_image_url(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.url_image_ht:
            return self.url_image_ht
        return self.url_image

    def get_audio_url(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.url_audio_ht:
            return self.url_audio_ht
        return self.url_audio

    def get_pdf_url(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.url_pdf_ht:
            return self.url_pdf_ht
        return self.url_pdf

    def get_lien_url(self, lang=None):
        if lang is None:
            lang = get_language()
        if lang == 'ht' and self.url_lien_ht:
            return self.url_lien_ht
        return self.url_lien
