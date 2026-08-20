from django.contrib import admin
from .models import Quiz, Question, Reponse, TentativeQuiz, ReponseUtilisateur


class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True
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
    list_display = ('titre', 'get_niveau_display', 'pourcentage_reussite', 'publie', 'created_at')
    list_filter = ('publie',)
    search_fields = ('titre', 'description', 'cours__titre', 'module__titre', 'lecon__titre')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'publie', 'pourcentage_reussite')
        }),
        ('Relasyon', {
            'fields': ('cours', 'module', 'lecon'),
            'description': 'Chwazi youn nan twa: Cours, Module, oswa Leçon. Se sèlman youn ki dwe ranpli.'
        }),
        ('Média du Quiz', {
            'fields': (
                'media_titre',
                'media_audio_url', 'media_audio_file',
                'media_video_url', 'media_video_file',
                'media_image_url', 'media_image_file',
                'media_texte'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_niveau_display(self, obj):
        niveau = obj.get_niveau()
        labels = {
            'cours': '📚 Cours',
            'module': '📖 Module',
            'lecon': '📝 Leçon',
            'inconnu': '❓ Inconnu',
        }
        return labels.get(niveau, niveau)
    get_niveau_display.short_description = "Niveau"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'texte', 'type_question', 'points', 'ordre')
    list_filter = ('type_question',)
    search_fields = ('texte', 'quiz__titre')
    list_editable = ('points', 'ordre')
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
    list_display = ('utilisateur', 'quiz', 'score', 'reussi', 'date_debut', 'date_soumission')
    list_filter = ('reussi',)
    search_fields = ('utilisateur__email', 'quiz__titre')
    readonly_fields = ('date_debut', 'date_soumission')


@admin.register(ReponseUtilisateur)
class ReponseUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('tentative', 'question', 'get_reponse_display')
    search_fields = ('tentative__utilisateur__email', 'question__texte')
    readonly_fields = ('audio_reponse', 'video_reponse', 'image_reponse', 'fichier_reponse')
    
    def get_reponse_display(self, obj):
        if obj.reponses_selectionnees.exists():
            return ", ".join([r.texte[:30] for r in obj.reponses_selectionnees.all()])
        if obj.texte_reponse:
            return obj.texte_reponse[:50]
        if obj.audio_reponse:
            return "🎵 Audio"
        if obj.video_reponse:
            return "🎬 Vidéo"
        if obj.image_reponse:
            return "🖼️ Image"
        if obj.fichier_reponse:
            return "📁 Fichier"
        return "—"
    get_reponse_display.short_description = "Réponse"