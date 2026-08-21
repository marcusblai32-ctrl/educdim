from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required
from .models import Quiz, Question, Reponse, TentativeQuiz, ReponseUtilisateur
from .services import corriger_tentative, get_upload_fields_for_question


def quiz_list(request):
    quizzes = Quiz.objects.filter(publie=True)
    return render(request, 'quiz/list.html', {'quizzes': quizzes})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'quiz/detail.html', {'quiz': quiz})


@login_required
def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    tentative = TentativeQuiz.objects.filter(
        utilisateur=request.user, quiz=quiz, date_soumission__isnull=True
    ).first()
    if not tentative:
        tentative = TentativeQuiz.objects.create(utilisateur=request.user, quiz=quiz)
    return redirect('quiz:take_quiz', tentative_pk=tentative.pk)


@login_required
def take_quiz(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)
    if tentative.date_soumission:
        messages.warning(request, _("Ce quiz a déjà été soumis."))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)
    questions = tentative.quiz.questions.all().order_by('ordre')
    total_questions = questions.count()
    reponses_utilisateur = {
        ru.question_id: ru for ru in ReponseUtilisateur.objects.filter(tentative=tentative)
    }

    # Pase durée quiz la (an minit)
    quiz_duree = tentative.quiz.duree_quiz if tentative.quiz.duree_quiz else 15

    return render(request, 'quiz/take_quiz.html', {
        'tentative': tentative,
        'questions': questions,
        'total_questions': total_questions,
        'reponses_utilisateur': reponses_utilisateur,
        'quiz_duree': quiz_duree,
    })


@login_required
def submit_quiz(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)
    if tentative.date_soumission:
        messages.warning(request, _("Ce quiz a déjà été soumis."))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)
    if request.method == 'POST':
        questions = tentative.quiz.questions.all()
        for question in questions:
            reponse_utilisateur, created = ReponseUtilisateur.objects.get_or_create(
                tentative=tentative, question=question
            )
            if question.type_question in ['single', 'vrai_faux']:
                reponse_id = request.POST.get(f'question_{question.id}')
                if reponse_id:
                    reponse = get_object_or_404(Reponse, pk=reponse_id)
                    reponse_utilisateur.reponses_selectionnees.set([reponse])
                else:
                    reponse_utilisateur.reponses_selectionnees.clear()
            elif question.type_question == 'multiple':
                reponse_ids = request.POST.getlist(f'question_{question.id}')
                if reponse_ids:
                    reponses = Reponse.objects.filter(pk__in=reponse_ids)
                    reponse_utilisateur.reponses_selectionnees.set(reponses)
                else:
                    reponse_utilisateur.reponses_selectionnees.clear()
            elif question.type_question == 'texte_trous':
                reponse_utilisateur.texte_reponse = request.POST.get(f'question_{question.id}_texte', '').strip()
            elif question.type_question == 'texte_libre':
                reponse_utilisateur.texte_reponse = request.POST.get(f'question_{question.id}_texte_libre', '').strip()
            elif question.type_question == 'audio_reponse':
                if request.FILES.get(f'question_{question.id}_audio'):
                    reponse_utilisateur.audio_reponse = request.FILES[f'question_{question.id}_audio']
                elif request.FILES.get(f'question_{question.id}_audio_upload'):
                    reponse_utilisateur.audio_reponse = request.FILES[f'question_{question.id}_audio_upload']
            elif question.type_question == 'video_reponse':
                if request.FILES.get(f'question_{question.id}_video'):
                    reponse_utilisateur.video_reponse = request.FILES[f'question_{question.id}_video']
            elif question.type_question == 'image_reponse':
                if request.FILES.get(f'question_{question.id}_image'):
                    reponse_utilisateur.image_reponse = request.FILES[f'question_{question.id}_image']
            elif question.type_question == 'fichier_reponse':
                if request.FILES.get(f'question_{question.id}_fichier'):
                    reponse_utilisateur.fichier_reponse = request.FILES[f'question_{question.id}_fichier']
            reponse_utilisateur.save()
        corriger_tentative(tentative)
        messages.success(request, _("Quiz soumis avec succès!"))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)
    return redirect('quiz:take_quiz', tentative_pk=tentative.pk)


@login_required
def quiz_result(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)
    if not tentative.date_soumission:
        messages.warning(request, _("Vous n'avez pas encore soumis ce quiz."))
        return redirect('quiz:take_quiz', tentative_pk=tentative.pk)
    reponses_utilisateur = ReponseUtilisateur.objects.filter(tentative=tentative).select_related('question')
    return render(request, 'quiz/result.html', {
        'tentative': tentative,
        'reponses_utilisateur': reponses_utilisateur,
    })


def get_question_upload_type(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    upload_info = get_upload_fields_for_question(question)
    if upload_info:
        return JsonResponse({'field_name': upload_info[0], 'label': upload_info[1], 'accept': upload_info[2], 'accept_mime': upload_info[3]})
    return JsonResponse({'error': 'Not an upload type'}, status=400)


# ===== NOUVO: VUE POU KOREKSYON STAFF =====
@staff_member_required
def tentative_list(request):
    """Lis tout tentatives soumises."""
    tentatives = TentativeQuiz.objects.filter(date_soumission__isnull=False).select_related('utilisateur', 'quiz')
    return render(request, 'quiz/correction/tentative_list.html', {'tentatives': tentatives})


@staff_member_required
def corriger_tentative_view(request, tentative_pk):  # <--- Non chanje
    """Koreksyon yon tentative espesifik."""
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, date_soumission__isnull=False)
    questions = tentative.quiz.questions.all().order_by('ordre')
    reponses_utilisateur = ReponseUtilisateur.objects.filter(tentative=tentative).select_related('question')

    if request.method == 'POST':
        for ru in reponses_utilisateur:
            points_key = f'points_{ru.id}'
            if points_key in request.POST:
                val = request.POST[points_key].strip()
                ru.points_attribues = float(val) if val else None
                ru.save()
        # Rekalkile nòt la
        corriger_tentative(tentative)
        messages.success(request, _("Koreksyon anrejistre epi nòt rekalkile."))
        return redirect('quiz:corriger_tentative', tentative_pk=tentative.pk)

    # Prepare done pou template
    question_data = []
    for q in questions:
        ru = next((r for r in reponses_utilisateur if r.question_id == q.id), None)
        selected_reponses = ru.reponses_selectionnees.all() if ru else []
        upload_fields = {
            'audio': ru.audio_reponse if ru else None,
            'video': ru.video_reponse if ru else None,
            'image': ru.image_reponse if ru else None,
            'fichier': ru.fichier_reponse if ru else None,
            'texte': ru.texte_reponse if ru else None,
        }
        question_data.append({
            'question': q,
            'reponse_utilisateur': ru,
            'selected_reponses': selected_reponses,
            'upload_fields': upload_fields,
        })

    return render(request, 'quiz/correction/corriger_tentative.html', {
        'tentative': tentative,
        'question_data': question_data,
    })