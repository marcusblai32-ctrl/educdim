from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Quiz, TentativeQuiz, ReponseUtilisateur
from .services import corriger_tentative
from enrollments.models import Enrollment
from courses.models import Lecon

@login_required
def quiz_list(request):
    cours_ids = Enrollment.objects.filter(utilisateur=request.user, statut='active').values_list('cours_id', flat=True)
    quizzes = Quiz.objects.filter(publie=True, cours_id__in=cours_ids)

    quizzes_reussi = TentativeQuiz.objects.filter(
        utilisateur=request.user,
        reussi=True
    ).values_list('quiz_id', flat=True)

    return render(request, 'quiz/quiz_list.html', {
        'quiz_list': quizzes,
        'quizzes_reussi': quizzes_reussi,
    })

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    tentatives = TentativeQuiz.objects.filter(utilisateur=request.user, quiz=quiz).order_by('-date_debut')
    deja_passe = tentatives.filter(reussi=True).exists()
    tentative_en_cours = tentatives.filter(date_soumission__isnull=True).first()

    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'tentatives': tentatives,
        'deja_passe': deja_passe,
        'tentative_en_cours': tentative_en_cours,
    })

@login_required
def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    # Verifye si deja reyisi
    if TentativeQuiz.objects.filter(utilisateur=request.user, quiz=quiz, reussi=True).exists():
        messages.warning(request, _("Vous avez déjà réussi ce quiz."))
        return redirect('quiz:detail', pk=quiz.pk)

    # Verifye si gen yon tentativ an kou
    existing = TentativeQuiz.objects.filter(utilisateur=request.user, quiz=quiz, date_soumission__isnull=True).first()
    if existing:
        return redirect('quiz:take_quiz', tentative_pk=existing.pk)

    tentative = TentativeQuiz.objects.create(utilisateur=request.user, quiz=quiz)
    return redirect('quiz:take_quiz', tentative_pk=tentative.pk)

@login_required
def take_quiz(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)

    if tentative.date_soumission:
        messages.error(request, _("Ce quiz a déjà été soumis."))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)

    questions = tentative.quiz.questions.all().prefetch_related('reponses')
    return render(request, 'quiz/take_quiz.html', {
        'tentative': tentative,
        'questions': questions
    })

@login_required
def submit_quiz(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)

    if tentative.date_soumission:
        messages.error(request, _("Quiz déjà soumis."))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)

    # Verifye si tout kesyon yo reponn
    questions = tentative.quiz.questions.all()
    total_questions = questions.count()
    answered = 0

    for question in questions:
        if question.type_question in ['single', 'vrai_faux', 'multiple']:
            ids = request.POST.getlist(f'question_{question.pk}')
            if ids:
                answered += 1
        elif question.type_question == 'texte_trous':
            if request.POST.get(f'question_{question.pk}', '').strip():
                answered += 1

    if answered < total_questions:
        messages.warning(request, _(f"Vous n'avez répondu qu'à {answered}/{total_questions} questions. Veuillez répondre à toutes les questions."))
        return redirect('quiz:take_quiz', tentative_pk=tentative.pk)

    ReponseUtilisateur.objects.filter(tentative=tentative).delete()

    for question in questions:
        ru = ReponseUtilisateur.objects.create(tentative=tentative, question=question)
        if question.type_question in ['single', 'vrai_faux', 'multiple']:
            ids = request.POST.getlist(f'question_{question.pk}')
            if ids:
                ru.reponses_selectionnees.set([int(aid) for aid in ids])
        elif question.type_question == 'texte_trous':
            ru.texte_reponse = request.POST.get(f'question_{question.pk}', '')
        ru.save()

    corriger_tentative(tentative)
    messages.success(request, _("Quiz soumis avec succès."))
    return redirect('quiz:quiz_result', tentative_pk=tentative.pk)

@login_required
def quiz_result(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)

    lecon = Lecon.objects.filter(quiz=tentative.quiz).first()

    context = {
        'tentative': tentative,
        'lecon': lecon,
        'deja_passe': True,
    }

    if tentative.reussi and lecon:
        messages.success(request, _("Félicitations ! Vous avez réussi le quiz. Vous pouvez continuer la leçon."))

    return render(request, 'quiz/quiz_result.html', context)
