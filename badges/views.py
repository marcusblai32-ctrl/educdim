from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Badge, BadgeUtilisateur

@login_required
def badge_list(request):
    badges = Badge.objects.filter(actif=True)
    return render(request, 'badges/badge_list.html', {'badges': badges})

@login_required
def my_badges(request):
    badges_utilisateur = BadgeUtilisateur.objects.filter(utilisateur=request.user).select_related('badge')
    return render(request, 'badges/my_badges.html', {'badges_utilisateur': badges_utilisateur})

@login_required
def badge_detail(request, pk):
    badge = get_object_or_404(Badge, pk=pk)
    return render(request, 'badges/badge_detail.html', {'badge': badge})
