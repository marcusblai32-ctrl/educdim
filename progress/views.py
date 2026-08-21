from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import Count, Q
from courses.models import Course, Lecon
from quiz.models import TentativeQuiz
from .models import ProgresCours, ProgresLecon, ActiviteUtilisateur


# ============================================
# DASHBOARD
# ============================================
@login_required
def dashboard(request):
    """Dashboard pwogresis itilizatè a"""
    user = request.user
    
    # Pwogresis tout kou yo
    progres_cours = ProgresCours.objects.filter(utilisateur=user).select_related('cours')
    
    # Estatistik
    total_cours = progres_cours.count()
    completed_cours = progres_cours.filter(pourcentage=100).count()
    
    # Lecon
    total_lecons = ProgresLecon.objects.filter(utilisateur=user).count()
    lecons_termine = ProgresLecon.objects.filter(utilisateur=user, statut='termine').count()
    lecons_en_cours = ProgresLecon.objects.filter(utilisateur=user, statut='en_cours').count()
    
    # Aktivite resan
    activites = ActiviteUtilisateur.objects.filter(
        utilisateur=user
    ).order_by('-date')[:20]
    
    # Kou an kou
    cours_en_cours = progres_cours.filter(
        pourcentage__gt=0,
        pourcentage__lt=100
    ).order_by('-date_modification')[:5]
    
    # Kou ki fini
    cours_termines = progres_cours.filter(pourcentage=100).order_by('-date_modification')[:5]
    
    context = {
        'progres_cours': progres_cours,
        'total_cours': total_cours,
        'completed_cours': completed_cours,
        'total_lecons': total_lecons,
        'lecons_termine': lecons_termine,
        'lecons_en_cours': lecons_en_cours,
        'activites': activites,
        'cours_en_cours': cours_en_cours,
        'cours_termines': cours_termines,
    }
    
    return render(request, 'progress/dashboard.html', context)


# ============================================
# COURSE PROGRESS
# ============================================
@login_required
def course_progress(request, course_pk):
    """Pwogresis itilizatè a nan yon kou espesifik"""
    cours = get_object_or_404(Course, pk=course_pk)
    
    progres_cours, created = ProgresCours.objects.get_or_create(
        utilisateur=request.user,
        cours=cours
    )
    
    # Mete ajou pwogresis
    progres_cours.mettre_a_jour()
    
    # Jwenn tout lecon yo
    lecons = Lecon.objects.filter(
        module__unite__cours=cours,
        actif=True
    ).order_by('module__unite__ordre', 'module__ordre', 'ordre')
    
    # Jwenn pwogresis chak lecon
    lecons_data = []
    for lecon in lecons:
        progres, _ = ProgresLecon.objects.get_or_create(
            utilisateur=request.user,
            lecon=lecon
        )
        lecons_data.append({
            'lecon': lecon,
            'progres': progres,
        })
    
    # Pwochen lecon
    prochain_lecon = progres_cours.get_prochain_lecon()
    
    context = {
        'cours': cours,
        'progres_cours': progres_cours,
        'lecons_data': lecons_data,
        'prochain_lecon': prochain_lecon,
    }
    
    return render(request, 'progress/course_progress.html', context)


# ============================================
# MARK LESSON COMPLETE
# ============================================
@login_required
def mark_lecon_complete(request, lecon_pk):
    """Mache yon lecon kòm fini epi mete ajou pwogresis"""
    lecon = get_object_or_404(Lecon, pk=lecon_pk)
    
    # Jwenn oswa kreye pwogresis lecon
    progres_lecon, created = ProgresLecon.objects.get_or_create(
        utilisateur=request.user,
        lecon=lecon
    )
    
    # Si deja fini, redirect
    if progres_lecon.est_termine():
        messages.info(request, _("Cette leçon est déjà terminée."))
        return redirect('courses:lesson_detail', pk=lecon_pk)
    
    # ===== VERIFYE QUIZ =====
    quizzes = lecon.quiz.all()  # Si ManyToManyField
    
    all_passed = True
    for quiz in quizzes:
        passed = TentativeQuiz.objects.filter(
            utilisateur=request.user,
            quiz=quiz,
            reussi=True
        ).exists()
        if not passed:
            all_passed = False
            break
    
    if not all_passed and quizzes.exists():
        messages.warning(
            request, 
            _("Vous devez réussir tous les quiz de cette leçon avant de la terminer.")
        )
        return redirect('courses:lesson_detail', pk=lecon_pk)
    
    # Mache lecon fini
    progres_lecon.terminer()
    
    # Ajoute aktivite
    ActiviteUtilisateur.objects.create(
        utilisateur=request.user,
        type_activite='lecon_termine',
        description=f"Leçon terminée: {lecon.titre}",
        cours=lecon.module.unite.cours,
        lecon=lecon
    )
    
    messages.success(request, _("Félicitations! Leçon terminée avec succès."))
    return redirect('courses:lesson_detail', pk=lecon_pk)


# ============================================
# START LESSON
# ============================================
@login_required
def start_lecon(request, lecon_pk):
    """Mache yon lecon kòm an kou"""
    lecon = get_object_or_404(Lecon, pk=lecon_pk)
    
    progres_lecon, created = ProgresLecon.objects.get_or_create(
        utilisateur=request.user,
        lecon=lecon
    )
    
    progres_lecon.commencer()
    
    # Ajoute aktivite
    ActiviteUtilisateur.objects.get_or_create(
        utilisateur=request.user,
        type_activite='lecon_commence',
        cours=lecon.module.unite.cours,
        lecon=lecon,
        defaults={
            'description': f"Leçon commencée: {lecon.titre}"
        }
    )
    
    return redirect('courses:lesson_detail', pk=lecon_pk)