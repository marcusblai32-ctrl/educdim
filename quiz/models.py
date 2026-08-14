from django.db import models
from django.conf import settings
from courses.models import Course

class Quiz(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    publie = models.BooleanField(default=False)
    pourcentage_reussite = models.PositiveIntegerField(default=70)
    created_at = models.DateTimeField(auto_now_add=True)

    # Medya miltip
    media_audio_url = models.URLField(blank=True, verbose_name="URL Audio")
    media_audio_file = models.FileField(upload_to='quiz/media/audio/', blank=True, null=True, verbose_name="Fichier Audio")
    media_video_url = models.URLField(blank=True, verbose_name="URL Vidéo")
    media_video_file = models.FileField(upload_to='quiz/media/video/', blank=True, null=True, verbose_name="Fichier Vidéo")
    media_image_url = models.URLField(blank=True, verbose_name="URL Image")
    media_image_file = models.ImageField(upload_to='quiz/media/images/', blank=True, null=True, verbose_name="Fichier Image")
    media_texte = models.TextField(blank=True, verbose_name="Texte du média")
    media_titre = models.CharField(max_length=200, blank=True, verbose_name="Titre du média")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

    def has_media(self):
        return any([
            self.media_audio_url, self.media_audio_file,
            self.media_video_url, self.media_video_file,
            self.media_image_url, self.media_image_file,
            self.media_texte
        ])

class Question(models.Model):
    TYPES_QUESTION = [
        ('single', 'Choix unique'),
        ('multiple', 'Choix multiples'),
        ('vrai_faux', 'Vrai/Faux'),
        ('texte_trous', 'Texte à trous'),
        ('audio_comprehension', 'Compréhension audio'),
        ('video_comprehension', 'Compréhension vidéo'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    type_question = models.CharField(max_length=25, choices=TYPES_QUESTION)
    texte = models.TextField()
    explication = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=1)
    ordre = models.PositiveIntegerField(default=1)

    # Medya miltip pou kesyon
    q_media_audio_url = models.URLField(blank=True, verbose_name="URL Audio")
    q_media_audio_file = models.FileField(upload_to='quiz/questions/audio/', blank=True, null=True, verbose_name="Fichier Audio")
    q_media_video_url = models.URLField(blank=True, verbose_name="URL Vidéo")
    q_media_video_file = models.FileField(upload_to='quiz/questions/video/', blank=True, null=True, verbose_name="Fichier Vidéo")
    q_media_image_url = models.URLField(blank=True, verbose_name="URL Image")
    q_media_image_file = models.ImageField(upload_to='quiz/questions/images/', blank=True, null=True, verbose_name="Fichier Image")
    q_media_texte = models.TextField(blank=True, verbose_name="Texte du média")
    q_media_titre = models.CharField(max_length=200, blank=True, verbose_name="Titre du média")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['quiz', 'ordre']

    def __str__(self):
        return f"{self.quiz.titre} - Q{self.ordre}: {self.texte[:50]}"

    def has_media(self):
        return any([
            self.q_media_audio_url, self.q_media_audio_file,
            self.q_media_video_url, self.q_media_video_file,
            self.q_media_image_url, self.q_media_image_file,
            self.q_media_texte
        ])

class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=500)
    est_correcte = models.BooleanField(default=False)
    ordre = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        ordering = ['question', 'ordre']

    def __str__(self):
        return f"{self.question.texte[:30]} -> {self.texte}"

class TentativeQuiz(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tentatives_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tentatives')
    date_debut = models.DateTimeField(auto_now_add=True)
    date_soumission = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reussi = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name = "Tentative de quiz"
        verbose_name_plural = "Tentatives de quiz"

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.quiz.titre} ({self.score}%)"

class ReponseUtilisateur(models.Model):
    tentative = models.ForeignKey(TentativeQuiz, on_delete=models.CASCADE, related_name='reponses_utilisateur')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reponses_selectionnees = models.ManyToManyField(Reponse, blank=True)
    texte_reponse = models.TextField(blank=True)

    class Meta:
        unique_together = ('tentative', 'question')
        verbose_name = "Réponse de l'utilisateur"
        verbose_name_plural = "Réponses des utilisateurs"

    def __str__(self):
        return f"{self.tentative.utilisateur.get_full_name()} - {self.question.texte[:30]}"
