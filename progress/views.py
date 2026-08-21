from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from courses.models import Course, Lecon, Module, Unite
from quiz.models import TentativeQuiz, ReponseUtilisateur
from .models import ProgressionUtilisateur, LeconTerminee, ActiviteUtilisateur, Certificat
from badges.models import Badge, BadgeObtenu
from django.contrib.auth import get_user_model

User = get_user_model()


# ============================================
# DASHBOARD PROGRESSION
# ============================================
@login_required
def dashboard(request):
    """Dashboard pwogresis itilizatè a"""
    user = request.user
    
    # Pwogresis tout kou yo
    progressions = ProgressionUtilisateur.objects.filter(utilisateur=user).select_related('cours')
    
    # Estatistik jeneral
    total_cours = progressions.count()
    completed_cours = progressions.filter(pourcentage=100).count()
    total_lecons_termine = LeconTerminee.objects.filter(utilisateur=user).count()
    
    # Dènye aktivite
    dernieres_activites = ActiviteUtilisateur.objects.filter(
        utilisateur=user
    ).order_by('-date')[:10]
    
    # Kou an kou
    cours_en_cours = progressions.filter(
        pourcentage__gt=0,
        pourcentage__lt=100
    ).order_by('-derniere_activite')[:5]
    
    # Kou ki fini
    cours_termines = progressions.filter(pourcentage=100).order_by('-date_modification')[:5]
    
    # Quiz ki fini yo
    tentatives_reussies = TentativeQuiz.objects.filter(
        utilisateur=user,
        reussi=True
    ).select_related('quiz').order_by('-date_soumission')[:10]
    
    # Badges obtenus
    badges_obtenus = BadgeObtenu.objects.filter(
        utilisateur=user
    ).select_related('badge').order_by('-date_obtenu')[:6]
    
    # Certificats
    certificats = Certificat.objects.filter(
        utilisateur=user
    ).order_by('-date_obtenu')[:5]
    
    context = {
        'progressions': progressions,
        'total_cours': total_cours,
        'completed_cours': completed_cours,
        'total_lecons_termine': total_lecons_termine,
        'dernieres_activites': dernieres_activites,
        'cours_en_cours': cours_en_cours,
        'cours_termines': cours_termines,
        'tentatives_reussies': tentatives_reussies,
        'badges_obtenus': badges_obtenus,
        'certificats': certificats,
    }
    
    return render(request, 'progress/dashboard.html', context)


# ============================================
# COURSE PROGRESS
# ============================================
@login_required
def course_progress(request, course_pk):
    """Pwogresis itilizatè a nan yon kou espesifik"""
    cours = get_object_or_404(Course, pk=course_pk)
    progression, created = ProgressionUtilisateur.objects.get_or_create(
        utilisateur=request.user,
        cours=cours
    )
    
    # Jwenn tout lecon yo nan kou a
    lecons = Lecon.objects.filter(
        module__unite__cours=cours,
        actif=True
    ).select_related('module__unite')
    
    # Lecon ki fini yo
    lecons_termine = LeconTerminee.objects.filter(
        utilisateur=request.user,
        lecon__in=lecons
    ).values_list('lecon_id', flat=True)
    
    # Quiz ki reyisi yo
    quizzes_reussi = TentativeQuiz.objects.filter(
        utilisateur=request.user,
        quiz__lecons__in=lecons,
        reussi=True
    ).values_list('quiz_id', flat=True).distinct()
    
    # Estatistik detaye
    total_lecons = lecons.count()
    lecons_fait = lecons_termine.count()
    pourcentage = int((lecons_fait / total_lecons * 100) if total_lecons > 0 else 0)
    
    # Mete ajou pwogresis
    if progression.pourcentage != pourcentage:
        progression.pourcentage = pourcentage
        progression.save()
    
    # Kou anvan ak apre
    previous_course = cours.get_previous_course()
    next_course = cours.get_next_course()
    
    # Estatistik quiz
    total_quiz = TentativeQuiz.objects.filter(
        quiz__lecons__in=lecons
    ).distinct().count()
    
    quiz_reussi_count = quizzes_reussi.count()
    
    context = {
        'cours': cours,
        'progression': progression,
        'lecons': lecons,
        'lecons_termine': lecons_termine,
        'quizzes_reussi': quizzes_reussi,
        'total_lecons': total_lecons,
        'lecons_fait': lecons_fait,
        'pourcentage': pourcentage,
        'previous_course': previous_course,
        'next_course': next_course,
        'total_quiz': total_quiz,
        'quiz_reussi_count': quiz_reussi_count,
    }
    
    return render(request, 'progress/course_progress.html', context)


# ============================================
# MARK LESSON COMPLETE - KORIJE
# ============================================
@login_required
def mark_lecon_complete(request, lecon_pk):
    """Mache yon lecon kòm fini epi mete ajou pwogresis"""
    lecon = get_object_or_404(Lecon, pk=lecon_pk)
    
    # ===== KORIJE: Verifye si relasyon an se ManyToManyField oswa ForeignKey =====
    # Si ManyToManyField:
    quizzes = lecon.quiz.all()
    
    # Si ForeignKey, itilize: quiz = lecon.quiz (sans .all())
    # Chwazi youn selon modèl ou a
    
    # Verifye si tout quiz yo reyisi
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
    
    # Make lecon complete
    lecon_terminee, created = LeconTerminee.objects.get_or_create(
        utilisateur=request.user,
        lecon=lecon
    )
    
    if created:
        # Ajoute aktivite
        ActiviteUtilisateur.objects.create(
            utilisateur=request.user,
            type_activite='lecon_terminee',
            description=f"Leçon terminée: {lecon.titre}",
            cours=lecon.module.unite.cours,
            lecon=lecon
        )
        
        # Vérifye badges
        check_badges(request.user, lecon.module.unite.cours)
    
    # Update progress
    progression, _ = ProgressionUtilisateur.objects.get_or_create(
        utilisateur=request.user,
        cours=lecon.module.unite.cours
    )
    progression.mettre_a_jour_pourcentage()
    
    messages.success(request, _("Félicitations! Leçon terminée avec succès."))
    return redirect('courses:lesson_detail', pk=lecon_pk)


# ============================================
# CHECK BADGES
# ============================================
def check_badges(user, cours):
    """Vérifye si itilizatè a merite nouvo badges"""
    # Badge premye lecon
    if not BadgeObtenu.objects.filter(utilisateur=user, badge__slug='premiere-lecon').exists():
        lecons_termine = LeconTerminee.objects.filter(utilisateur=user).count()
        if lecons_termine >= 1:
            badge = Badge.objects.filter(slug='premiere-lecon').first()
            if badge:
                BadgeObtenu.objects.create(
                    utilisateur=user,
                    badge=badge,
                    cours=cours
                )
    
    # Badge 10 lecons
    if not BadgeObtenu.objects.filter(utilisateur=user, badge__slug='dix-lecons').exists():
        lecons_termine = LeconTerminee.objects.filter(utilisateur=user).count()
        if lecons_termine >= 10:
            badge = Badge.objects.filter(slug='dix-lecons').first()
            if badge:
                BadgeObtenu.objects.create(
                    utilisateur=user,
                    badge=badge,
                    cours=cours
                )
    
    # Badge cours complete
    if not BadgeObtenu.objects.filter(utilisateur=user, badge__slug='cours-complete').exists():
        progression = ProgressionUtilisateur.objects.filter(
            utilisateur=user,
            pourcentage=100
        ).count()
        if progression >= 1:
            badge = Badge.objects.filter(slug='cours-complete').first()
            if badge:
                BadgeObtenu.objects.create(
                    utilisateur=user,
                    badge=badge,
                    cours=cours
                )


# ============================================
# USER ACTIVITY
# ============================================
@login_required
def user_activity(request):
    """Lis tout aktivite itilizatè a"""
    activites = ActiviteUtilisateur.objects.filter(
        utilisateur=request.user
    ).order_by('-date')
    
    return render(request, 'progress/activity_list.html', {
        'activites': activites
    })


# ============================================
# CERTIFICATS
# ============================================
@login_required
def certificat_list(request):
    """Lis tout certificat itilizatè a"""
    certificats = Certificat.objects.filter(
        utilisateur=request.user
    ).order_by('-date_obtenu')
    
    return render(request, 'progress/certificat_list.html', {
        'certificats': certificats
    })


@login_required
def certificat_detail(request, certificat_pk):
    """Detay yon certificat"""
    certificat = get_object_or_404(Certificat, pk=certificat_pk, utilisateur=request.user)
    return render(request, 'progress/certificat_detail.html', {
        'certificat': certificat
    })


# ============================================
# STATISTIQUES PROGRESSION
# ============================================
@login_required
def stats_progression(request):
    """Estatistik detaye sou pwogresis itilizatè a"""
    user = request.user
    
    # Kou total
    total_cours = Course.objects.filter(publie=True).count()
    cours_inscrit = ProgressionUtilisateur.objects.filter(utilisateur=user).count()
    
    # Lecon
    total_lecons = Lecon.objects.filter(actif=True).count()
    lecons_termine = LeconTerminee.objects.filter(utilisateur=user).count()
    
    # Quiz
    total_quiz = TentativeQuiz.objects.filter(utilisateur=user).count()
    quiz_reussi = TentativeQuiz.objects.filter(utilisateur=user, reussi=True).count()
    
    # Temps (si w gen yon modèl pou sa)
    # ...
    
    context = {
        'total_cours': total_cours,
        'cours_inscrit': cours_inscrit,
        'total_lecons': total_lecons,
        'lecons_termine': lecons_termine,
        'total_quiz': total_quiz,
        'quiz_reussi': quiz_reussi,
    }
    
    return render(request, 'progress/stats.html', context)