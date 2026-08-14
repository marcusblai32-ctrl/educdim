from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Niveau, PointsUtilisateur, HistoriquePoints

@login_required
def leaderboard(request):
    top_total = PointsUtilisateur.objects.order_by('-total')[:20]
    top_semaine = PointsUtilisateur.objects.order_by('-semaine')[:20]
    top_mois = PointsUtilisateur.objects.order_by('-mois')[:20]
    return render(request, 'ranking/leaderboard.html', {
        'top_total': top_total,
        'top_semaine': top_semaine,
        'top_mois': top_mois,
    })

@login_required
def my_rank(request):
    points, created = PointsUtilisateur.objects.get_or_create(utilisateur=request.user)
    niveaux = Niveau.objects.all().order_by('-points_min')
    niveau_actuel = None
    prochain_niveau = None
    for niveau in niveaux:
        if points.total >= niveau.points_min:
            niveau_actuel = niveau
            break
    if niveau_actuel:
        prochain_niveau = Niveau.objects.filter(points_min__gt=niveau_actuel.points_min).order_by('points_min').first()
    historique = HistoriquePoints.objects.filter(utilisateur=request.user)[:30]
    return render(request, 'ranking/my_rank.html', {
        'points': points,
        'niveau_actuel': niveau_actuel,
        'prochain_niveau': prochain_niveau,
        'historique': historique,
    })
