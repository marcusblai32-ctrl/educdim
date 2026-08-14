from django.contrib import admin
from .models import Theme

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'primary', 'secondary', 'actif', 'maintenance_mode')
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'site_name', 'site_description', 'logo', 'favicon', 'actif')
        }),

        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),

        ('Contenu - Hero', {
            'fields': (
                'hero_title', 'hero_subtitle', 'hero_badge', 'hero_subtitle_line2',
                'btn_explore', 'btn_start', 'hero_image',
                'stats_etudiants', 'stats_cours', 'stats_satisfaction'
            )
        }),

        # ===== NOUVEAU: HERO CARDS =====
        ('Hero - Cartes', {
            'fields': (
                'hero_card1_title', 'hero_card1_desc', 'hero_card1_icon',
                'hero_card2_title', 'hero_card2_desc', 'hero_card2_icon',
                'hero_card3_title', 'hero_card3_desc', 'hero_card3_icon'
            ),
            'description': 'Personnalisez les cartes qui apparaissent à droite du Hero'
        }),

        ('Contenu - Features', {
            'fields': (
                'features_tag', 'features_title', 'features_highlight',
                'feature1_title', 'feature1_desc', 'feature1_icon', 'feature1_color',
                'feature2_title', 'feature2_desc', 'feature2_icon', 'feature2_color',
                'feature3_title', 'feature3_desc', 'feature3_icon', 'feature3_color',
                'feature_link_text'
            )
        }),

        ('Contenu - CTA', {
            'fields': ('cta_title', 'cta_highlight', 'cta_desc', 'cta_btn')
        }),

        ('Contenu - Témoignages', {
            'fields': (
                'testimonials_tag', 'testimonials_title', 'testimonials_highlight', 'testimonials_end',
                'testimonial1_text', 'testimonial1_name', 'testimonial1_job', 'testimonial1_avatar', 'testimonial1_stars',
                'testimonial2_text', 'testimonial2_name', 'testimonial2_job', 'testimonial2_avatar', 'testimonial2_stars'
            )
        }),

        ('Pied de page', {
            'fields': ('footer_text', 'about_text', 'contact_email')
        }),

        ('Pages - Contact', {
            'fields': ('contact_page_title', 'contact_page_subtitle', 'contact_phone', 'contact_address', 'contact_hours', 'contact_map_embed')
        }),

        ('Pages - À propos', {
            'fields': ('about_title', 'about_content', 'about_image')
        }),

        ('Pages - Conditions', {
            'fields': ('conditions_title', 'conditions_content')
        }),

        ('Pages - Confidentialité', {
            'fields': ('privacy_title', 'privacy_content')
        }),

        ('Pages - FAQ', {
            'fields': ('faq_title', 'faq_content')
        }),

        # ===== NOUVEAU: EVENEMENT =====
        ('Événement', {
            'fields': (
                'evenement_actif', 'evenement_banner', 'evenement_nom',
                'evenement_logo', 'evenement_message', 'evenement_hashtag'
            ),
            'description': 'Activez un événement spécial pour afficher une bannière sur le site'
        }),

        ('Maintenance & WhatsApp', {
            'fields': ('maintenance_mode', 'maintenance_message', 'whatsapp_group', 'whatsapp_contact')
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

        ('Typographie', {
            'fields': ('font_family', 'border_radius', 'box_shadow')
        }),
    )