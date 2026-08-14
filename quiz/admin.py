from django.contrib import admin
from .models import Quiz, Question, Reponse, TentativeQuiz, ReponseUtilisateur

class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fieldsets = (
        (None, {'fields': ('type_question', 'texte', 'explication', 'points', 'ordre')}),
        ('Média de la question', {
            'fields': (
                'q_media_titre',
                'q_media_audio_url', 'q_media_audio_file',
                'q_media_video_url', 'q_media_video_file',
                'q_media_image_url', 'q_media_image_file',
                'q_media_texte'
            ),
            'classes': ('collapse',)
        }),
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'pourcentage_reussite', 'publie')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {'fields': ('cours', 'titre', 'description', 'publie', 'pourcentage_reussite')}),
        ('Média du Quiz', {
            'fields': (
                'media_titre',
                'media_audio_url', 'media_audio_file',
                'media_video_url', 'media_video_file',
                'media_image_url', 'media_image_file',
                'media_texte'
            )
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'texte', 'type_question', 'points')
    inlines = [ReponseInline]
    fieldsets = (
        (None, {'fields': ('quiz', 'type_question', 'texte', 'explication', 'points', 'ordre')}),
        ('Média de la question', {
            'fields': (
                'q_media_titre',
                'q_media_audio_url', 'q_media_audio_file',
                'q_media_video_url', 'q_media_video_file',
                'q_media_image_url', 'q_media_image_file',
                'q_media_texte'
            ),
            'classes': ('collapse',)
        }),
    )

@admin.register(TentativeQuiz)
class TentativeQuizAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'quiz', 'score', 'reussi', 'date_soumission')

@admin.register(ReponseUtilisateur)
class ReponseUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('tentative', 'question')
