from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import SessionPresence, FichePresence, JustificationAbsence

@login_required
def student_attendance(request):
    fiches = FichePresence.objects.filter(utilisateur=request.user).select_related('session')
    return render(request, 'attendance/student_list.html', {'fiches': fiches})

@login_required
def session_detail(request, pk):
    session = get_object_or_404(SessionPresence, pk=pk)
    context = {'session': session}
    if request.user.is_staff:
        context['fiches'] = session.fiches.all()
    else:
        ma_fiche = FichePresence.objects.filter(session=session, utilisateur=request.user).first()
        context['ma_fiche'] = ma_fiche
        if ma_fiche:
            context['justification'] = JustificationAbsence.objects.filter(fiche=ma_fiche).first()
    return render(request, 'attendance/session_detail.html', context)

@login_required
def submit_justification(request, fiche_pk):
    fiche = get_object_or_404(FichePresence, pk=fiche_pk, utilisateur=request.user)
    if JustificationAbsence.objects.filter(fiche=fiche).exists():
        messages.error(request, _("Une justification existe déjà."))
        return redirect('attendance:session_detail', pk=fiche.session.pk)
    if request.method == 'POST':
        raison = request.POST.get('raison')
        if raison:
            JustificationAbsence.objects.create(fiche=fiche, raison=raison)
            messages.success(request, _("Justification soumise avec succès."))
            return redirect('attendance:session_detail', pk=fiche.session.pk)
    return render(request, 'attendance/justification_form.html', {'fiche': fiche})

@user_passes_test(lambda u: u.is_staff)
def review_justification(request, pk):
    justification = get_object_or_404(JustificationAbsence, pk=pk)
    if request.method == 'POST':
        justification.examinee = True
        justification.approuvee = request.POST.get('approuvee') == 'on'
        justification.note_admin = request.POST.get('note_admin', '')
        justification.save()
        messages.success(request, _("Justification révisée."))
        return redirect('attendance:session_detail', pk=justification.fiche.session.pk)
    return render(request, 'attendance/review_justification.html', {'justification': justification})
