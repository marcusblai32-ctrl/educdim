from django.contrib import admin
from .models import Course, Unite, Module, Lecon, SectionLecon, Contenu, Category, Niveau, Promotions

class UniteInline(admin.TabularInline):
    model = Unite
    extra = 0

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0

class LeconInline(admin.TabularInline):
    model = Lecon
    extra = 0

class SectionInline(admin.TabularInline):
    model = SectionLecon
    extra = 0

class ContenuInline(admin.TabularInline):
    model = Contenu
    extra = 0
    fields = ('type_contenu', 'titre', 'titre_ht', 'ordre')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'ordre')
    search_fields = ('nom',)

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nivo', 'date_debut', 'date_fin', 'actif')
    filter_horizontal = ('etudiants',)
    search_fields = ('nom',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'publie', 'categorie', 'nivo', 'created_at')
    list_filter = ('publie', 'categorie', 'nivo', 'inscription_ouverte')
    search_fields = ('titre', 'description')
    inlines = [UniteInline]
    fieldsets = (
        ('Informations générales', {'fields': ('titre', 'description', 'image_url', 'image', 'prix', 'publie', 'created_by')}),
        ('Catégorisation', {'fields': ('categorie', 'nivo', 'duree')}),
        ('Inscriptions', {'fields': ('inscription_ouverte', 'date_debut_inscription', 'date_fin_inscription', 'promotion')}),
    )

@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'ordre', 'actif')
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'unite', 'ordre', 'actif')
    inlines = [LeconInline]

@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'ordre', 'actif', 'quiz')
    inlines = [SectionInline]

@admin.register(SectionLecon)
class SectionLeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'lecon', 'type_section', 'ordre')
    inlines = [ContenuInline]

@admin.register(Contenu)
class ContenuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'section', 'type_contenu', 'ordre')
    fieldsets = (
        (None, {'fields': ('section', 'type_contenu', 'ordre')}),
        ('Version Française', {'fields': ('titre', 'texte', 'url_video', 'url_image', 'url_audio', 'url_pdf', 'url_lien')}),
        ('Version Créole', {'fields': ('titre_ht', 'texte_ht', 'url_video_ht', 'url_image_ht', 'url_audio_ht', 'url_pdf_ht', 'url_lien_ht')}),
        ('Fichiers locaux (optionnel)', {'fields': ('fichier_audio', 'image', 'fichier_pdf', 'fichier'), 'classes': ('collapse',)}),
    )
