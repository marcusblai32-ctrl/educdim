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

    pourcentage = (points_obtenus / total_points * 100) if total_points > 0 else 0
    tentative.score = pourcentage
    tentative.reussi = pourcentage >= tentative.quiz.pourcentage_reussite
    tentative.date_soumission = timezone.now()
    tentative.save()
    return pourcentage
