from django.contrib import admin
from django.utils.html import format_html
from .models import Theme

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'maintenance_mode', 'evenement_actif')
    list_filter = ('actif', 'maintenance_mode', 'evenement_actif')
    search_fields = ('nom', 'site_name', 'meta_description')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'site_name', 'site_description', 'actif')
        }),
        ('Logo & Favicon', {
            'fields': ('logo', 'logo_url', 'favicon', 'favicon_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Couleurs principales', {
            'fields': ('primary', 'primary_hover', 'secondary', 'secondary_hover')
        }),
        ("Couleurs d'état", {
            'fields': ('success', 'success_hover', 'danger', 'danger_hover', 'warning', 'warning_hover', 'info', 'info_hover')
        }),
        ('Fond et texte', {
            'fields': ('body_bg', 'text_color', 'text_muted', 'white', 'light', 'dark', 'border')
        }),
        ('Typographie et style', {
            'fields': ('font_family', 'border_radius', 'box_shadow')
        }),
        ('Section Hero', {
            'fields': (
                'hero_title', 'hero_subtitle', 'hero_badge', 'hero_subtitle_line2',
                'btn_explore', 'btn_start', 'hero_image', 'hero_image_url',
                'stats_etudiants', 'stats_cours', 'stats_satisfaction'
            )
        }),
        ('Hero - Cartes', {
            'fields': (
                'hero_card1_title', 'hero_card1_desc', 'hero_card1_icon',
                'hero_card2_title', 'hero_card2_desc', 'hero_card2_icon',
                'hero_card3_title', 'hero_card3_desc', 'hero_card3_icon'
            ),
            'description': 'Personnalisez les cartes qui apparaissent à droite du Hero'
        }),
        ('Section Features', {
            'fields': (
                'features_tag', 'features_title', 'features_highlight',
                'feature1_title', 'feature1_desc', 'feature1_icon', 'feature1_color',
                'feature2_title', 'feature2_desc', 'feature2_icon', 'feature2_color',
                'feature3_title', 'feature3_desc', 'feature3_icon', 'feature3_color',
                'feature_link_text'
            )
        }),
        ('Section CTA', {
            'fields': ('cta_title', 'cta_highlight', 'cta_desc', 'cta_btn')
        }),
        ('Section Témoignages', {
            'fields': (
                'testimonials_tag', 'testimonials_title', 'testimonials_highlight', 'testimonials_end',
                'testimonial1_text', 'testimonial1_name', 'testimonial1_job', 'testimonial1_avatar', 'testimonial1_stars',
                'testimonial2_text', 'testimonial2_name', 'testimonial2_job', 'testimonial2_avatar', 'testimonial2_stars'
            )
        }),
        ('Page - À propos', {
            'fields': ('about_title', 'about_content', 'about_image', 'about_image_url'),
            'classes': ('collapse',)
        }),
        ('Page - Contact', {
            'fields': ('contact_page_title', 'contact_page_subtitle', 'contact_phone', 'contact_address', 'contact_hours', 'contact_map_embed'),
            'classes': ('collapse',)
        }),
        ('Page - Conditions générales', {
            'fields': ('conditions_title', 'conditions_content'),
            'classes': ('collapse',)
        }),
        ('Page - Confidentialité', {
            'fields': ('privacy_title', 'privacy_content'),
            'classes': ('collapse',)
        }),
        ('Page - FAQ', {
            'fields': ('faq_title', 'faq_content'),
            'classes': ('collapse',)
        }),
        ('Pied de page', {
            'fields': ('footer_text', 'about_text', 'contact_email')
        }),
        ('Événement spécial', {
            'fields': (
                'evenement_actif', 'evenement_banner', 'evenement_banner_url',
                'evenement_nom', 'evenement_logo', 'evenement_logo_url',
                'evenement_message', 'evenement_hashtag'
            ),
            'description': 'Activez un événement spécial pour afficher une bannière sur le site'
        }),
        ('Maintenance & WhatsApp', {
            'fields': ('maintenance_mode', 'maintenance_message', 'whatsapp_group', 'whatsapp_contact'),
            'classes': ('collapse',)
        }),
    )
