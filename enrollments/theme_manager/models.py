from django.db import models

class Theme(models.Model):
    # ===== COULEURS =====
    nom = models.CharField(max_length=100, default="Thème principal", verbose_name="Nom")
    primary = models.CharField(max_length=7, default="#2563eb", verbose_name="Primaire")
    primary_hover = models.CharField(max_length=7, default="#1d4ed8", verbose_name="Primaire hover")
    secondary = models.CharField(max_length=7, default="#64748b", verbose_name="Secondaire")
    secondary_hover = models.CharField(max_length=7, default="#475569", verbose_name="Secondaire hover")
    success = models.CharField(max_length=7, default="#10b981", verbose_name="Succès")
    success_hover = models.CharField(max_length=7, default="#059669", verbose_name="Succès hover")
    danger = models.CharField(max_length=7, default="#ef4444", verbose_name="Danger")
    danger_hover = models.CharField(max_length=7, default="#dc2626", verbose_name="Danger hover")
    warning = models.CharField(max_length=7, default="#f59e0b", verbose_name="Avertissement")
    warning_hover = models.CharField(max_length=7, default="#d97706", verbose_name="Avertissement hover")
    info = models.CharField(max_length=7, default="#06b6d4", verbose_name="Info")
    info_hover = models.CharField(max_length=7, default="#0891b2", verbose_name="Info hover")
    light = models.CharField(max_length=7, default="#f8fafc", verbose_name="Clair")
    dark = models.CharField(max_length=7, default="#0f172a", verbose_name="Foncé")
    body_bg = models.CharField(max_length=7, default="#f1f5f9", verbose_name="Fond de page")
    text_color = models.CharField(max_length=7, default="#1e293b", verbose_name="Couleur texte")
    text_muted = models.CharField(max_length=7, default="#64748b", verbose_name="Texte secondaire")
    white = models.CharField(max_length=7, default="#ffffff", verbose_name="Blanc")
    border = models.CharField(max_length=7, default="#e2e8f0", verbose_name="Bordure")
    font_family = models.CharField(max_length=200, default="'Inter', 'Segoe UI', sans-serif", verbose_name="Police")
    border_radius = models.CharField(max_length=10, default="12px", verbose_name="Rayon bordures")
    box_shadow = models.CharField(max_length=100, default="0 4px 6px -1px rgba(0,0,0,0.1)", verbose_name="Ombre")

    # ===== SITE INFO =====
    logo = models.ImageField(upload_to='theme/', blank=True, null=True, verbose_name="Logo (fichier)")
    logo_url = models.URLField(blank=True, null=True, verbose_name="Logo (URL externe)")
    favicon = models.ImageField(upload_to='theme/', blank=True, null=True, verbose_name="Favicon (fichier)")
    favicon_url = models.URLField(blank=True, null=True, verbose_name="Favicon (URL externe)")
    site_name = models.CharField(max_length=200, default="EduPlatform", verbose_name="Nom du site")
    site_description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")

    # ===== SEO =====
    meta_description = models.TextField(blank=True, default="EduPlatform - Platform e-learning pou aprann san limit.", verbose_name="Meta Description")
    meta_keywords = models.CharField(max_length=200, blank=True, default="e-learning, cours en ligne, éducation", verbose_name="Meta Keywords")

    # ===== HERO SECTION =====
    hero_title = models.CharField(max_length=200, blank=True, default="Apprenez sans limites", verbose_name="Titre Hero")
    hero_subtitle = models.TextField(blank=True, default="Des cours de qualité pour développer vos compétences à votre rythme.", verbose_name="Sous-titre Hero")
    hero_badge = models.CharField(max_length=200, blank=True, default="Plateforme e-learning", verbose_name="Badge Hero")
    hero_subtitle_line2 = models.CharField(max_length=200, blank=True, default="Où que vous soyez", verbose_name="Sous-titre ligne 2")
    btn_explore = models.CharField(max_length=100, blank=True, default="Explorer les cours", verbose_name="Bouton Explorer")
    btn_start = models.CharField(max_length=100, blank=True, default="Commencer gratuitement", verbose_name="Bouton Démarrer")
    hero_image = models.ImageField(upload_to='theme/hero/', blank=True, null=True, verbose_name="Image Hero (fichier)")
    hero_image_url = models.URLField(blank=True, null=True, verbose_name="Image Hero (URL externe)")
    stats_etudiants = models.PositiveIntegerField(default=1200, verbose_name="Étudiants")
    stats_cours = models.PositiveIntegerField(default=50, verbose_name="Cours")
    stats_satisfaction = models.PositiveIntegerField(default=95, verbose_name="Satisfaction")

    # ===== HERO CARDS =====
    hero_card1_title = models.CharField(max_length=200, blank=True, default="Formation en ligne", verbose_name="Hero Carte 1 Titre")
    hero_card1_desc = models.CharField(max_length=200, blank=True, default="+1000 étudiants", verbose_name="Hero Carte 1 Description")
    hero_card1_icon = models.CharField(max_length=50, blank=True, default="fas fa-laptop-code", verbose_name="Hero Carte 1 Icône")

    hero_card2_title = models.CharField(max_length=200, blank=True, default="Certifiés", verbose_name="Hero Carte 2 Titre")
    hero_card2_desc = models.CharField(max_length=200, blank=True, default="Reconnus par l'État", verbose_name="Hero Carte 2 Description")
    hero_card2_icon = models.CharField(max_length=50, blank=True, default="fas fa-certificate", verbose_name="Hero Carte 2 Icône")

    hero_card3_title = models.CharField(max_length=200, blank=True, default="+50 cours", verbose_name="Hero Carte 3 Titre")
    hero_card3_desc = models.CharField(max_length=200, blank=True, default="Disponibles", verbose_name="Hero Carte 3 Description")
    hero_card3_icon = models.CharField(max_length=50, blank=True, default="fas fa-users", verbose_name="Hero Carte 3 Icône")

    # ===== FEATURES SECTION =====
    features_tag = models.CharField(max_length=200, blank=True, default="Pourquoi nous choisir ?", verbose_name="Tag Features")
    features_title = models.CharField(max_length=200, blank=True, default="Une expérience d'apprentissage", verbose_name="Titre Features")
    features_highlight = models.CharField(max_length=100, blank=True, default="unique", verbose_name="Surlignage Features")

    feature1_title = models.CharField(max_length=200, blank=True, default="Cours interactifs", verbose_name="Feature 1 Titre")
    feature1_desc = models.TextField(blank=True, default="Apprenez avec des vidéos, quiz et exercices pratiques conçus pour vous.", verbose_name="Feature 1 Desc")
    feature1_icon = models.CharField(max_length=50, blank=True, default="fas fa-laptop-code", verbose_name="Feature 1 Icône")
    feature1_color = models.CharField(max_length=50, blank=True, default="primary", verbose_name="Feature 1 Couleur")

    feature2_title = models.CharField(max_length=200, blank=True, default="Certificats vérifiés", verbose_name="Feature 2 Titre")
    feature2_desc = models.TextField(blank=True, default="Recevez des certificats reconnus après chaque cours complété avec succès.", verbose_name="Feature 2 Desc")
    feature2_icon = models.CharField(max_length=50, blank=True, default="fas fa-certificate", verbose_name="Feature 2 Icône")
    feature2_color = models.CharField(max_length=50, blank=True, default="success", verbose_name="Feature 2 Couleur")

    feature3_title = models.CharField(max_length=200, blank=True, default="Classement & Badges", verbose_name="Feature 3 Titre")
    feature3_desc = models.TextField(blank=True, default="Gagnez des points, débloquez des badges et grimpez dans le classement.", verbose_name="Feature 3 Desc")
    feature3_icon = models.CharField(max_length=50, blank=True, default="fas fa-trophy", verbose_name="Feature 3 Icône")
    feature3_color = models.CharField(max_length=50, blank=True, default="warning", verbose_name="Feature 3 Couleur")

    feature_link_text = models.CharField(max_length=100, blank=True, default="En savoir plus", verbose_name="Feature Lien Texte")

    # ===== CTA SECTION =====
    cta_title = models.CharField(max_length=200, blank=True, default="Prêt à commencer votre", verbose_name="CTA Titre")
    cta_highlight = models.CharField(max_length=100, blank=True, default="aventure", verbose_name="CTA Surlignage")
    cta_desc = models.TextField(blank=True, default="Rejoignez des milliers d'apprenants et transformez votre avenir dès aujourd'hui.", verbose_name="CTA Desc")
    cta_btn = models.CharField(max_length=100, blank=True, default="Créer un compte gratuit", verbose_name="CTA Bouton")

    # ===== TESTIMONIALS SECTION =====
    testimonials_tag = models.CharField(max_length=200, blank=True, default="Ce que nos étudiants disent", verbose_name="Tag Témoignages")
    testimonials_title = models.CharField(max_length=200, blank=True, default="Ils ont", verbose_name="Titre Témoignages")
    testimonials_highlight = models.CharField(max_length=100, blank=True, default="réussi", verbose_name="Surlignage Témoignages")
    testimonials_end = models.CharField(max_length=100, blank=True, default="grâce à nous", verbose_name="Fin Témoignages")

    testimonial1_text = models.TextField(blank=True, default="Grâce à EduPlatform, j'ai appris le développement web en 3 mois. Aujourd'hui je travaille comme freelance.", verbose_name="Témoignage 1 Texte")
    testimonial1_name = models.CharField(max_length=100, blank=True, default="Jean Dupont", verbose_name="Témoignage 1 Nom")
    testimonial1_job = models.CharField(max_length=100, blank=True, default="Développeur Web", verbose_name="Témoignage 1 Métier")
    testimonial1_avatar = models.URLField(blank=True, default="https://ui-avatars.com/api/?name=Jean+Dupont&background=2563eb&color=fff&size=50", verbose_name="Témoignage 1 Avatar")
    testimonial1_stars = models.PositiveIntegerField(default=5, verbose_name="Témoignage 1 Étoiles")

    testimonial2_text = models.TextField(blank=True, default="Les cours sont bien structurés et les professeurs sont très compétents. Je recommande à 100%.", verbose_name="Témoignage 2 Texte")
    testimonial2_name = models.CharField(max_length=100, blank=True, default="Marie Paul", verbose_name="Témoignage 2 Nom")
    testimonial2_job = models.CharField(max_length=100, blank=True, default="Data Analyst", verbose_name="Témoignage 2 Métier")
    testimonial2_avatar = models.URLField(blank=True, default="https://ui-avatars.com/api/?name=Marie+Paul&background=10b981&color=fff&size=50", verbose_name="Témoignage 2 Avatar")
    testimonial2_stars = models.PositiveIntegerField(default=5, verbose_name="Témoignage 2 Étoiles")

    # ===== FOOTER =====
    footer_text = models.CharField(max_length=200, blank=True, default="Tous droits réservés", verbose_name="Texte pied page")
    about_text = models.TextField(blank=True, verbose_name="À propos")
    contact_email = models.EmailField(blank=True, verbose_name="Email contact")

    # ===== PAGES =====
    contact_page_title = models.CharField(max_length=200, blank=True, default="Contactez-nous", verbose_name="Titre page contact")
    contact_page_subtitle = models.TextField(blank=True, default="Nous sommes là pour vous aider. Envoyez-nous un message.", verbose_name="Sous-titre contact")
    contact_phone = models.CharField(max_length=50, blank=True, default="+509 0000-0000", verbose_name="Téléphone")
    contact_address = models.TextField(blank=True, default="Port-au-Prince, Haïti", verbose_name="Adresse")
    contact_hours = models.CharField(max_length=200, blank=True, default="Lun-Ven: 8h - 17h", verbose_name="Heures")
    contact_map_embed = models.TextField(blank=True, verbose_name="Google Maps")

    about_title = models.CharField(max_length=200, blank=True, default="À propos de nous", verbose_name="Titre À propos")
    about_content = models.TextField(blank=True, default="<p>EduPlatform se yon platform e-learning ki fèt pou ede moun aprann san limit.</p><p>Misyon nou se bay tout moun aksè a edikasyon kalite.</p>", verbose_name="Contenu À propos (HTML)")
    about_image = models.ImageField(upload_to='theme/about/', blank=True, null=True, verbose_name="Image À propos (fichier)")
    about_image_url = models.URLField(blank=True, null=True, verbose_name="Image À propos (URL externe)")

    conditions_title = models.CharField(max_length=200, blank=True, default="Conditions générales", verbose_name="Titre conditions")
    conditions_content = models.TextField(blank=True, default="<h3>1. Acceptation</h3><p>En utilisant notre plateforme, vous acceptez ces conditions.</p><h3>2. Compte</h3><p>Vous êtes responsable de votre compte.</p>", verbose_name="Contenu conditions")

    privacy_title = models.CharField(max_length=200, blank=True, default="Politique de confidentialité", verbose_name="Titre confidentialité")
    privacy_content = models.TextField(blank=True, default="<h3>1. Collecte des données</h3><p>Nous collectons certaines données.</p><h3>2. Utilisation</h3><p>Vos données ne sont pas partagées.</p>", verbose_name="Contenu confidentialité")

    faq_title = models.CharField(max_length=200, blank=True, default="Questions fréquentes", verbose_name="Titre FAQ")
    faq_content = models.TextField(blank=True, default="<h4>Comment m'inscrire ?</h4><p>Klike sou bouton S'inscrire.</p><h4>Les cours sont-ils payants ?</h4><p>Gen kou gratis ak kou peye.</p>", verbose_name="Contenu FAQ (HTML)")

    # ===== MAINTENANCE & WHATSAPP =====
    maintenance_mode = models.BooleanField(default=False, verbose_name="Mode maintenance")
    maintenance_message = models.TextField(blank=True, default="L'équipe travaille sur le site. Veuillez patienter, nous revenons bientôt !", verbose_name="Message maintenance")
    whatsapp_group = models.CharField(max_length=100, blank=True, default="", verbose_name="Numéro WhatsApp groupe")
    whatsapp_contact = models.CharField(max_length=100, blank=True, default="", verbose_name="Numéro WhatsApp contact")

    # ===== EVENEMENT =====
    evenement_actif = models.BooleanField(default=False, verbose_name="Événement actif")
    evenement_banner = models.ImageField(upload_to='theme/evenements/', blank=True, null=True, verbose_name="Bannière événement (fichier)")
    evenement_banner_url = models.URLField(blank=True, null=True, verbose_name="Bannière événement (URL externe)")
    evenement_nom = models.CharField(max_length=200, blank=True, default="", verbose_name="Nom événement")
    evenement_logo = models.ImageField(upload_to='theme/evenements/', blank=True, null=True, verbose_name="Logo événement (fichier)")
    evenement_logo_url = models.URLField(blank=True, null=True, verbose_name="Logo événement (URL externe)")
    evenement_message = models.TextField(blank=True, default="", verbose_name="Message événement")
    evenement_hashtag = models.CharField(max_length=100, blank=True, default="", verbose_name="Hashtag événement")

    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"

    def save(self, *args, **kwargs):
        if self.actif:
            Theme.objects.filter(actif=True).exclude(pk=self.pk).update(actif=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    # ===== METHOD POU JWEN IMAJ (Fichier oswa URL) =====
    def get_logo(self):
        return self.logo.url if self.logo and self.logo.name else self.logo_url

    def get_favicon(self):
        return self.favicon.url if self.favicon and self.favicon.name else self.favicon_url

    def get_hero_image(self):
        return self.hero_image.url if self.hero_image and self.hero_image.name else self.hero_image_url

    def get_about_image(self):
        return self.about_image.url if self.about_image and self.about_image.name else self.about_image_url

    def get_evenement_banner(self):
        return self.evenement_banner.url if self.evenement_banner and self.evenement_banner.name else self.evenement_banner_url

    def get_evenement_logo(self):
        return self.evenement_logo.url if self.evenement_logo and self.evenement_logo.name else self.evenement_logo_url
