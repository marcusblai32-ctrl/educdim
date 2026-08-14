from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Q
from .models import Course, Unite, Module, Lecon, SectionLecon, Category, Niveau, LearningPath, CoursePrerequisite
from .forms import CourseForm
from enrollments.models import Enrollment
from quiz.models import TentativeQuiz
from subscriptions.models import SubscriptionAccess
from theme_manager.models import Theme


def course_list(request):
    cours = Course.objects.filter(publie=True)
    search_query = request.GET.get('search', '')
    if search_query:
        cours = cours.filter(Q(titre__icontains=search_query) | Q(description__icontains=search_query))

    category_id = request.GET.get('category')
    if category_id:
        cours = cours.filter(categorie_id=category_id)

    niveau_id = request.GET.get('niveau')
    if niveau_id:
        cours = cours.filter(nivo_id=niveau_id)

    prix_filter = request.GET.get('prix')
    if prix_filter == 'gratuit':
        cours = cours.filter(prix=0)
    elif prix_filter == 'payant':
        cours = cours.filter(prix__gt=0)

    learning_path_id = request.GET.get('learning_path')
    if learning_path_id:
        cours = cours.filter(learning_path_id=learning_path_id)

    categories = Category.objects.filter(actif=True)
    niveaux = Niveau.objects.all()
    learning_paths = LearningPath.objects.filter(actif=True)

    return render(request, 'courses/course_list.html', {
        'cours': cours,
        'categories': categories,
        'niveaux': niveaux,
        'learning_paths': learning_paths,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_niveau': niveau_id,
        'selected_prix': prix_filter,
        'selected_learning_path': learning_path_id,
    })


def course_detail(request, pk):
    cours = get_object_or_404(Course, pk=pk)
    est_inscrit = False
    inscription_approuvee = False
    a_acces_abonnement = False
    tentatives_quiz = []
    quizzes_reussi = []
    prerequis_completed = True
    prerequis_missing = []
    prerequisites = cours.get_prerequisites()

    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(utilisateur=request.user, cours=cours).first()
        if enrollment:
            est_inscrit = True
            if enrollment.statut == 'active':
                inscription_approuvee = True

        a_acces_abonnement = SubscriptionAccess.objects.filter(
            subscription__utilisateur=request.user,
            subscription__statut='active',
            cours=cours,
            date_expiration__gt=timezone.now()
        ).exists()

        if a_acces_abonnement:
            inscription_approuvee = True

        tentatives_quiz = TentativeQuiz.objects.filter(
            utilisateur=request.user,
            quiz__cours=cours
        ).select_related('quiz')
        quizzes_reussi = [t.quiz for t in tentatives_quiz if t.reussi]

        # Vérifier les prérequis
        if prerequisites:
            prerequis_completed, prerequis_missing = cours.get_prerequisites_completed(request.user)
    else:
        # Si itilizatè a pa konekte
        prerequis_completed = True
        prerequis_missing = []

    unites = cours.unites.filter(actif=True)

    # Cours précédent/suivant
    previous_course = cours.get_previous_course()
    next_course = cours.get_next_course()
    position_display = cours.get_position_display()

    # Récupérer les quizzes du cours
    quizzes = cours.quiz.filter(publie=True)

    # Récupérer les tentatives de l'utilisateur pour chaque quiz
    user_tentatives = {}
    if request.user.is_authenticated:
        for quiz in quizzes:
            tentative = quiz.tentatives.filter(utilisateur=request.user).order_by('-date_soumission').first()
            if tentative:
                user_tentatives[quiz.pk] = tentative

    return render(request, 'courses/course_detail.html', {
        'cours': cours,
        'unites': unites,
        'est_inscrit': est_inscrit,
        'inscription_approuvee': inscription_approuvee,
        'a_acces_abonnement': a_acces_abonnement,
        'tentatives_quiz': tentatives_quiz,
        'quizzes_reussi': quizzes_reussi,
        'prerequisites': prerequisites,
        'prerequis_completed': prerequis_completed,
        'prerequis_missing': prerequis_missing,
        'previous_course': previous_course,
        'next_course': next_course,
        'position_display': position_display,
        'quizzes': quizzes,
        'user_tentatives': user_tentatives,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, "Cours créé avec succès.")
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours mis à jour.")
            return redirect('courses:course_detail', pk=pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Cours supprimé.")
        return redirect('courses:course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_inscription(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.inscription_ouverte = not course.inscription_ouverte
    course.save()
    status = "ouvertes" if course.inscription_ouverte else "fermées"
    messages.success(request, f"Inscriptions {status} pour le cours '{course.titre}'.")
    return redirect('courses:course_detail', pk=pk)


def unit_detail(request, pk):
    unite = get_object_or_404(Unite, pk=pk)
    modules = unite.modules.filter(actif=True)
    return render(request, 'courses/unit_detail.html', {'unite': unite, 'modules': modules})


def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lecons = module.lecons.filter(actif=True)
    return render(request, 'courses/module_detail.html', {'module': module, 'lecons': lecons})


def lesson_detail(request, pk):
    lecon = get_object_or_404(Lecon, pk=pk)
    sections = lecon.sections.all()

    if request.user.is_authenticated and lecon.quiz:
        quiz_termine = TentativeQuiz.objects.filter(
            utilisateur=request.user,
            quiz=lecon.quiz,
            reussi=True
        ).exists()
        if not quiz_termine:
            messages.warning(request, "Vous devez terminer le quiz avant de voir cette leçon.")
            return redirect('quiz:detail', pk=lecon.quiz.pk)

    return render(request, 'courses/lesson_detail.html', {
        'lecon': lecon,
        'sections': sections
    })


def section_detail(request, pk):
    section = get_object_or_404(SectionLecon, pk=pk)
    contenus = section.contenus.all()
    return render(request, 'courses/section_detail.html', {'section': section, 'contenus': contenus})


def about_page(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'pages/about.html', {'theme': theme})


def contact_page(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'pages/contact.html', {'theme': theme})


def conditions_page(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'pages/conditions.html', {'theme': theme})


def privacy_page(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'pages/privacy.html', {'theme': theme})


def faq_page(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'pages/faq.html', {'theme': theme})


# ============================================
# LEARNING PATH VIEWS
# ============================================
def learning_path_list(request):
    learning_paths = LearningPath.objects.filter(actif=True)
    return render(request, 'courses/learning_path_list.html', {'learning_paths': learning_paths})


def learning_path_detail(request, pk):
    learning_path = get_object_or_404(LearningPath, pk=pk)
    cours = learning_path.cours_publies()
    return render(request, 'courses/learning_path_detail.html', {
        'learning_path': learning_path,
        'cours': cours,
    })