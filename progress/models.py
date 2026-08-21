from django.db import models
from django.conf import settings
from django.utils import timezone
from courses.models import Lecon, Course, Module, Unite
from quiz.models import TentativeQuiz


class ProgresLecon(models.Model):
    STATUT_CHOICES = [
        ('non_commence', 'Non commencée'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminée'),
    ]
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progres_lecons')
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE, related_name='progres')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_commence')
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('utilisateur', 'lecon')
        verbose_name = "Progrès de leçon"
        verbose_name_plural = "Progrès des leçons"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.lecon.titre} ({self.get_statut_display()})"
    
    def commencer(self):
        """Mache lecon kòm an kou"""
        if self.statut == 'non_commence':
            self.statut = 'en_cours'
            self.date_debut = timezone.now()
            self.save()
    
    def terminer(self):
        """Mache lecon kòm fini"""
        self.statut = 'termine'
        self.date_fin = timezone.now()
        self.save()
        
        # Mete ajou pwogresis kou a
        self.mettre_a_jour_progres_cours()
    
    def mettre_a_jour_progres_cours(self):
        """Mete ajou pousantaj pwogresis kou a"""
        cours = self.lecon.module.unite.cours
        progres_cours, _ = ProgresCours.objects.get_or_create(
            utilisateur=self.utilisateur,
            cours=cours
        )
        progres_cours.mettre_a_jour()
    
    def est_termine(self):
        return self.statut == 'termine'
    
    def est_en_cours(self):
        return self.statut == 'en_cours'


class ProgresCours(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progres_cours')
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progres')
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'cours')
        verbose_name = "Progrès de cours"
        verbose_name_plural = "Progrès des cours"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.cours.titre} : {self.pourcentage}%"
    
    def mettre_a_jour(self):
        """Rekalkile pousantaj pwogresis kou a"""
        # Jwenn tout lecon nan kou a
        lecons = Lecon.objects.filter(
            module__unite__cours=self.cours,
            actif=True
        )
        total_lecons = lecons.count()
        
        if total_lecons == 0:
            self.pourcentage = 0
            self.save()
            return
        
        # Jwenn lecon ki fini
        lecons_termine = ProgresLecon.objects.filter(
            utilisateur=self.utilisateur,
            lecon__in=lecons,
            statut='termine'
        ).count()
        
        # Kalkile pousantaj
        self.pourcentage = round((lecons_termine / total_lecons) * 100, 2)
        self.save()
        
        # Si kou a konplè, ajoute aktivite
        if self.pourcentage == 100:
            from .models import ActiviteUtilisateur  # Import lokal pou evite sik
            ActiviteUtilisateur.objects.get_or_create(
                utilisateur=self.utilisateur,
                type_activite='cours_termine',
                cours=self.cours,
                defaults={
                    'description': f"Cours terminé: {self.cours.titre}"
                }
            )
    
    def get_lecons_termine(self):
        """Retounen tout lecon ki fini nan kou a"""
        lecons = Lecon.objects.filter(module__unite__cours=self.cours)
        return ProgresLecon.objects.filter(
            utilisateur=self.utilisateur,
            lecon__in=lecons,
            statut='termine'
        )
    
    def get_lecons_en_cours(self):
        """Retounen tout lecon an kou nan kou a"""
        lecons = Lecon.objects.filter(module__unite__cours=self.cours)
        return ProgresLecon.objects.filter(
            utilisateur=self.utilisateur,
            lecon__in=lecons,
            statut='en_cours'
        )
    
    def get_prochain_lecon(self):
        """Retounen pwochen lecon ki poko fini"""
        lecons = Lecon.objects.filter(
            module__unite__cours=self.cours,
            actif=True
        ).order_by('module__unite__ordre', 'module__ordre', 'ordre')
        
        for lecon in lecons:
            progres, _ = ProgresLecon.objects.get_or_create(
                utilisateur=self.utilisateur,
                lecon=lecon
            )
            if not progres.est_termine():
                return lecon
        return None
    
    def est_termine(self):
        """Verifye si kou a fini"""
        return self.pourcentage == 100


class ActiviteUtilisateur(models.Model):
    TYPES_ACTIVITE = [
        ('connexion', 'Connexion'),
        ('lecon_commence', 'Leçon commencée'),
        ('lecon_termine', 'Leçon terminée'),
        ('quiz_termine', 'Quiz terminé'),
        ('quiz_reussi', 'Quiz réussi'),
        ('cours_termine', 'Cours terminé'),
        ('certificat_obtenu', 'Certificat obtenu'),
        ('badge_obtenu', 'Badge obtenu'),
    ]
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activites')
    type_activite = models.CharField(max_length=30, choices=TYPES_ACTIVITE)
    description = models.TextField(blank=True)
    cours = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='activites')
    lecon = models.ForeignKey(Lecon, on_delete=models.SET_NULL, null=True, blank=True, related_name='activites')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Activité utilisateur"
        verbose_name_plural = "Activités utilisateurs"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.get_type_activite_display()} - {self.date.strftime('%d/%m/%Y %H:%M')}"