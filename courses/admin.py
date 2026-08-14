from django.contrib import admin
from .models import (
    Course, Unite, Module, Lecon, SectionLecon, Contenu,
    Category, Niveau, Promotions, LearningPath, CoursePrerequisite
)


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


# ============================================
# LEARNING PATH ADMIN (NOUVEAU)
# ============================================
@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'nombre_cours')
    search_fields = ('nom', 'description')
    list_filter = ('actif',)


# ============================================
# COURSE PREREQUISITE ADMIN (NOUVEAU)
# ============================================
@admin.register(CoursePrerequisite)
class CoursePrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('cours', 'prerequis', 'obligatoire')
    search_fields = ('cours__titre', 'prerequis__titre')
    list_filter = ('obligatoire',)


# ============================================
# CATEGORY ADMIN (EXISTANT)
# ============================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'ordre')
    search_fields = ('nom',)


# ============================================
# NIVEAU ADMIN (EXISTANT)
# ============================================
@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)


# ============================================
# PROMOTIONS ADMIN (EXISTANT)
# ============================================
@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nivo', 'date_debut', 'date_fin', 'actif')
    filter_horizontal = ('etudiants',)
    search_fields = ('nom',)


# ============================================
# COURSE ADMIN (MODIFIÉ)
# ============================================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'publie', 'categorie', 'nivo', 'learning_path', 'position', 'created_at')
    list_filter = ('publie', 'categorie', 'nivo', 'inscription_ouverte', 'learning_path')
    search_fields = ('titre', 'description')
    inlines = [UniteInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'image_url', 'image', 'prix', 'publie', 'created_by')
        }),
        ('Catégorisation', {
            'fields': ('categorie', 'nivo', 'duree')
        }),
        ('Learning Path', {
            'fields': ('learning_path', 'position'),
            'classes': ('collapse',)
        }),
        ('Inscriptions', {
            'fields': ('inscription_ouverte', 'date_debut_inscription', 'date_fin_inscription', 'promotion')
        }),
    )


# ============================================
# UNITE ADMIN (EXISTANT)
# ============================================
@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'ordre', 'actif')
    inlines = [ModuleInline]


# ============================================
# MODULE ADMIN (EXISTANT)
# ============================================
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'unite', 'ordre', 'actif')
    inlines = [LeconInline]


# ============================================
# LECON ADMIN (EXISTANT)
# ============================================
@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module', 'ordre', 'actif', 'quiz')
    inlines = [SectionInline]


# ============================================
# SECTION LECON ADMIN (EXISTANT)
# ============================================
@admin.register(SectionLecon)
class SectionLeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'lecon', 'type_section', 'ordre')
    inlines = [ContenuInline]


# ============================================
# CONTENU ADMIN (EXISTANT)
# ============================================
@admin.register(Contenu)
class ContenuAdmin(admin.ModelAdmin):
    list_display = ('titre', 'section', 'type_contenu', 'ordre')
    fieldsets = (
        (None, {'fields': ('section', 'type_contenu', 'ordre')}),
        ('Version Française', {
            'fields': ('titre', 'texte', 'url_video', 'url_image', 'url_audio', 'url_pdf', 'url_lien')
        }),
        ('Version Créole', {
            'fields': ('titre_ht', 'texte_ht', 'url_video_ht', 'url_image_ht', 'url_audio_ht', 'url_pdf_ht', 'url_lien_ht')
        }),
        ('Fichiers locaux (optionnel)', {
            'fields': ('fichier_audio', 'image', 'fichier_pdf', 'fichier'),
            'classes': ('collapse',)
        }),
    )