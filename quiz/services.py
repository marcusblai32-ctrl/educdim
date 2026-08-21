from django.utils import timezone
from .models import ReponseUtilisateur

def corriger_tentative(tentative):
    total_points = 0
    points_obtenus = 0.0

    for question in tentative.quiz.questions.all():
        total_points += question.points

        try:
            reponse_utilisateur = ReponseUtilisateur.objects.get(tentative=tentative, question=question)
        except ReponseUtilisateur.DoesNotExist:
            continue

        # ===== NOUVO: Si gen pwen manyèl, itilize yo =====
        if reponse_utilisateur.points_attribues is not None:
            points_obtenus += float(reponse_utilisateur.points_attribues)
            continue
        # ===== FEN NOUVO =====

        # ===== TYPES AVEC REPONSES (CHOIX) =====
        if question.type_question in ['single', 'vrai_faux']:
            bonne_reponse = question.reponses.filter(est_correcte=True).first()
            if bonne_reponse and reponse_utilisateur.reponses_selectionnees.filter(pk=bonne_reponse.pk).exists():
                points_obtenus += question.points

        elif question.type_question == 'multiple':
            bonnes_reponses = set(question.reponses.filter(est_correcte=True).values_list('pk', flat=True))
            reponses_selectionnees = set(reponse_utilisateur.reponses_selectionnees.values_list('pk', flat=True))
            if bonnes_reponses == reponses_selectionnees:
                points_obtenus += question.points

        elif question.type_question == 'texte_trous':
            bonne_reponse = question.reponses.first()
            if bonne_reponse and reponse_utilisateur.texte_reponse.strip().lower() == bonne_reponse.texte.strip().lower():
                points_obtenus += question.points

        # ===== TYPES AVEC UPLOAD (Fichier, Audio, Video, Image) =====
        elif question.type_question in ['audio_reponse', 'video_reponse', 'image_reponse', 'fichier_reponse', 'texte_libre']:
            # Vérifier si l'utilisateur a bien envoyé quelque chose
            has_response = False
            if question.type_question == 'audio_reponse' and reponse_utilisateur.audio_reponse:
                has_response = True
            elif question.type_question == 'video_reponse' and reponse_utilisateur.video_reponse:
                has_response = True
            elif question.type_question == 'image_reponse' and reponse_utilisateur.image_reponse:
                has_response = True
            elif question.type_question == 'fichier_reponse' and reponse_utilisateur.fichier_reponse:
                has_response = True
            elif question.type_question == 'texte_libre' and reponse_utilisateur.texte_reponse:
                has_response = True

            # Pour l'instant, on ne donne pas de points automatiquement.
            # L'instructeur doit corriger manuellement.
            # On pourrait ajouter un champ "points_manuel" plus tard.
            if has_response:
                # On ne donne pas de points automatiquement
                pass

    pourcentage = (points_obtenus / total_points * 100) if total_points > 0 else 0
    tentative.score = pourcentage
    tentative.reussi = pourcentage >= tentative.quiz.pourcentage_reussite
    tentative.date_soumission = timezone.now()
    tentative.save()
    return pourcentage


def get_upload_fields_for_question(question):
    """Retourne les champs d'upload disponibles pour un type de question"""
    mapping = {
        'audio_reponse': ('audio_reponse', 'Enregistrement audio', 'audio/*', 'audio/mpeg, audio/wav'),
        'video_reponse': ('video_reponse', 'Enregistrement vidéo', 'video/*', 'video/mp4, video/webm'),
        'image_reponse': ('image_reponse', 'Télécharger une image', 'image/*', 'image/png, image/jpeg'),
        'fichier_reponse': ('fichier_reponse', 'Télécharger un fichier', '*/*', '.pdf, .doc, .docx, .txt'),
    }
    return mapping.get(question.type_question, None)