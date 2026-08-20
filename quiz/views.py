import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.core.files.base import ContentFile
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

    # Vérifier si une tentative en cours existe
    tentative = TentativeQuiz.objects.filter(
        utilisateur=request.user,
        quiz=quiz,
        date_soumission__isnull=True
    ).first()

    if not tentative:
        tentative = TentativeQuiz.objects.create(
            utilisateur=request.user,
            quiz=quiz
        )

    return redirect('quiz:take_quiz', tentative_pk=tentative.pk)


@login_required
def take_quiz(request, tentative_pk):
    tentative = get_object_or_404(TentativeQuiz, pk=tentative_pk, utilisateur=request.user)

    if tentative.date_soumission:
        messages.warning(request, _("Ce quiz a déjà été soumis."))
        return redirect('quiz:quiz_result', tentative_pk=tentative.pk)

    questions = tentative.quiz.questions.all().order_by('ordre')
    total_questions = questions.count()

    # Récupérer les réponses déjà enregistrées
    reponses_utilisateur = {
        ru.question_id: ru for ru in ReponseUtilisateur.objects.filter(tentative=tentative)
    }

    return render(request, 'quiz/take_quiz.html', {
        'tentative': tentative,
        'questions': questions,
        'total_questions': total_questions,
        'reponses_utilisateur': reponses_utilisateur,
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
                tentative=tentative,
                question=question
            )

            # ===== TRAITEMENT DES RÉPONSES =====
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
                texte = request.POST.get(f'question_{question.id}_texte', '').strip()
                reponse_utilisateur.texte_reponse = texte

            elif question.type_question == 'texte_libre':
                texte = request.POST.get(f'question_{question.id}_texte_libre', '').strip()
                reponse_utilisateur.texte_reponse = texte

            # ===== AUDIO RECORDING (Base64) =====
            elif question.type_question == 'audio_reponse':
                # TCHEK 1: Audio anrejistre nan navigatè (base64)
                audio_blob = request.POST.get(f'question_{question.id}_audio_blob', '')
                audio_filename = request.POST.get(f'question_{question.id}_audio_filename', '')
                
                if audio_blob:
                    try:
                        # Dekode base64 la
                        format_part, base64_data = audio_blob.split(';base64,')
                        audio_bytes = base64.b64decode(base64_data)
                        
                        # Sove fichye a
                        reponse_utilisateur.audio_reponse.save(
                            audio_filename,
                            ContentFile(audio_bytes),
                            save=False
                        )
                    except Exception as e:
                        messages.error(request, f"Erreur lors de l'enregistrement audio: {str(e)}")
                
                # TCHEK 2: Fichye telechaje
                elif request.FILES.get(f'question_{question.id}_audio'):
                    reponse_utilisateur.audio_reponse = request.FILES[f'question_{question.id}_audio']

            # ===== UPLOAD DES FICHIERS =====
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

        # Corriger le quiz
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

    # Récupérer les réponses pour afficher les corrections
    reponses_utilisateur = ReponseUtilisateur.objects.filter(tentative=tentative).select_related('question')

    return render(request, 'quiz/result.html', {
        'tentative': tentative,
        'reponses_utilisateur': reponses_utilisateur,
    })


def get_question_upload_type(request, question_id):
    """API pour récupérer le type d'upload d'une question"""
    question = get_object_or_404(Question, pk=question_id)
    upload_info = get_upload_fields_for_question(question)
    if upload_info:
        return JsonResponse({
            'field_name': upload_info[0],
            'label': upload_info[1],
            'accept': upload_info[2],
            'accept_mime': upload_info[3]
        })
    return JsonResponse({'error': 'Not an upload type'}, status=400)