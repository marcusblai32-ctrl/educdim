from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import ProgresLecon, ProgresCours
from courses.models import Course, Lecon
from enrollments.models import Enrollment
from quiz.models import TentativeQuiz

@login_required
def dashboard(request):
    user = request.user
    cours_ids = Enrollment.objects.filter(utilisateur=user, statut='active').values_list('cours_id', flat=True)
    progres_cours = ProgresCours.objects.filter(utilisateur=user, cours_id__in=cours_ids).select_related('cours')
    return render(request, 'progress/dashboard.html', {'progres_cours': progres_cours})

@login_required
def course_progress(request, pk):
    cours = get_object_or_404(Course, pk=pk)
    user = request.user
    lecons_data = []
    for unite in cours.unites.filter(actif=True):
        for module in unite.modules.filter(actif=True):
            for lecon in module.lecons.filter(actif=True):
                pl, _ = ProgresLecon.objects.get_or_create(utilisateur=user, lecon=lecon)
                lecons_data.append({'lecon': lecon, 'progres': pl})
    try:
        progres_global = ProgresCours.objects.get(utilisateur=user, cours=cours)
    except ProgresCours.DoesNotExist:
        progres_global = None
    return render(request, 'progress/course_progress.html', {
        'cours': cours,
        'lecons_data': lecons_data,
        'progres_global': progres_global,
    })

@login_required
def mark_lecon_complete(request, lecon_pk):
    lecon = get_object_or_404(Lecon, pk=lecon_pk)

    # Vérifier si le quiz est terminé avant de compléter
    if lecon.quiz:
        quiz_termine = TentativeQuiz.objects.filter(
            utilisateur=request.user,
            quiz=lecon.quiz,
            reussi=True
        ).exists()

        if not quiz_termine:
            messages.error(request, "Vous devez d'abord terminer le quiz de cette leçon.")
            return redirect('quiz:detail', pk=lecon.quiz.pk)

    pl, _ = ProgresLecon.objects.get_or_create(utilisateur=request.user, lecon=lecon)

    if pl.statut != 'termine':
        pl.statut = 'termine'
        pl.date_fin = timezone.now()
        pl.save()

        cours = lecon.module.unite.cours
        pc, _ = ProgresCours.objects.get_or_create(utilisateur=request.user, cours=cours)
        total = Lecon.objects.filter(module__unite__cours=cours, actif=True).count()
        completed = ProgresLecon.objects.filter(
            utilisateur=request.user,
            lecon__module__unite__cours=cours,
            statut='termine'
        ).count()
        pc.pourcentage = (completed / total * 100) if total > 0 else 0
        pc.save()

        messages.success(request, f"Leçon '{lecon.titre}' marquée comme terminée.")
    else:
        messages.info(request, "Cette leçon est déjà terminée.")

    return redirect('courses:lesson_detail', pk=lecon_pk)
