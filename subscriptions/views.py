from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import transaction
from .models import SubscriptionPlan, Subscription, SubscriptionAccess, SubscriptionCourseSelection
from .forms import SubscriptionForm, CourseSelectionForm


@login_required
def subscription_list(request):
    plans = SubscriptionPlan.objects.filter(actif=True)
    user_subscriptions = Subscription.objects.filter(utilisateur=request.user)
    active_sub = user_subscriptions.filter(statut='active').first()

    return render(request, 'subscriptions/list.html', {
        'plans': plans,
        'active_sub': active_sub,
        'user_subscriptions': user_subscriptions,
    })


@login_required
def subscribe(request, plan_pk):
    # ===== KORIJE: Jere si plan pa egziste =====
    try:
        plan = SubscriptionPlan.objects.get(pk=plan_pk, actif=True)
    except SubscriptionPlan.DoesNotExist:
        messages.error(request, _("Ce plan d'abonnement n'existe pas ou n'est plus disponible."))
        return redirect('subscriptions:list')

    existing = Subscription.objects.filter(
        utilisateur=request.user,
        plan=plan,
        statut__in=['pending', 'active']
    ).first()
    if existing:
        messages.info(request, _("Vous avez déjà une demande pour ce plan."))
        return redirect('subscriptions:list')

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.utilisateur = request.user
            subscription.plan = plan

            if request.user.is_staff and form.cleaned_data.get('methode_paiement') == 'manual':
                subscription.statut = 'active'
                subscription.date_debut = timezone.now()
                subscription.date_fin = timezone.now() + timezone.timedelta(days=plan.duree_jours)
                subscription.date_verification = timezone.now()
                subscription.verifie_par = request.user
                subscription.save()

                # ===== NOUVO WORKFLOW: Si max_courses > 0 =====
                try:
                    if plan.max_courses > 0:
                        messages.success(request, _("Abonnement activé ! Veuillez maintenant choisir vos cours."))
                        return redirect('subscriptions:select_courses', pk=subscription.pk)
                except AttributeError:
                    # max_courses pa egziste ankò, ansyen konpòtman
                    pass

                # ===== ANSYEN WORKFLOW: Si max_courses == 0 oswa pa egziste =====
                for cours in plan.cours.all():
                    SubscriptionAccess.objects.get_or_create(
                        subscription=subscription,
                        cours=cours,
                        defaults={'date_expiration': subscription.date_fin}
                    )
                
                try:
                    subscription.courses_selectionnes = True
                    subscription.save(update_fields=['courses_selectionnes'])
                except:
                    pass

                messages.success(request, _("Abonnement activé !"))
                return redirect('subscriptions:list')
            else:
                subscription.statut = 'pending'
                subscription.save()
                messages.success(request, _("Votre demande a été envoyée. Un administrateur vérifiera votre paiement."))
                return redirect('subscriptions:list')
    else:
        form = SubscriptionForm(user=request.user)

    return render(request, 'subscriptions/subscribe.html', {
        'form': form,
        'plan': plan,
    })


@login_required
def my_subscriptions(request):
    subscriptions = Subscription.objects.filter(utilisateur=request.user).order_by('-date_demande')
    return render(request, 'subscriptions/my_subscriptions.html', {'subscriptions': subscriptions})


@login_required
def subscription_detail(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, utilisateur=request.user)
    accesses = sub.accesses.all().select_related('cours')
    selections = sub.course_selections.all().select_related('course')
    return render(request, 'subscriptions/detail.html', {
        'subscription': sub,
        'accesses': accesses,
        'selections': selections,
    })


# ===== NOUVO VIEW: Chwazi kou yo =====
@login_required
def select_courses(request, pk):
    """Itilizatè chwazi kou yo pou abònman aktif li."""
    subscription = get_object_or_404(
        Subscription,
        pk=pk,
        utilisateur=request.user,
        statut='active'
    )

    # Si plan pa gen limit, redirect sou lis
    try:
        if subscription.plan.max_courses == 0:
            messages.info(request, _("Ce plan donne accès à tous les cours automatiquement."))
            return redirect('subscriptions:my_subscriptions')
    except AttributeError:
        messages.info(request, _("Ce plan donne accès à tous les cours automatiquement."))
        return redirect('subscriptions:my_subscriptions')

    # Si deja seleksyone, redirect
    if subscription.courses_selectionnes:
        messages.info(request, _("Vous avez déjà sélectionné vos cours."))
        return redirect('subscriptions:my_subscriptions')

    places_restantes = subscription.get_places_restantes()
    if places_restantes is not None and places_restantes <= 0:
        messages.warning(request, _("Vous avez atteint la limite de cours pour ce plan."))
        return redirect('subscriptions:my_subscriptions')

    if request.method == 'POST':
        form = CourseSelectionForm(request.POST, subscription=subscription)
        if form.is_valid():
            selected_courses = form.cleaned_data['courses']

            # Verifye limit
            if places_restantes is not None and selected_courses.count() > places_restantes:
                messages.error(
                    request,
                    _("Vous ne pouvez sélectionner que {} cours maximum.").format(places_restantes)
                )
            else:
                try:
                    with transaction.atomic():
                        # Kreye seleksyon yo
                        for course in selected_courses:
                            SubscriptionCourseSelection.objects.get_or_create(
                                subscription=subscription,
                                course=course
                            )
                            # Kreye aksè yo
                            SubscriptionAccess.objects.get_or_create(
                                subscription=subscription,
                                cours=course,
                                defaults={'date_expiration': subscription.date_fin}
                            )

                        # Verifye si tout plas yo ranpli
                        places_restantes_apres = subscription.get_places_restantes()
                        if places_restantes_apres is not None and places_restantes_apres == 0:
                            subscription.courses_selectionnes = True
                            subscription.save(update_fields=['courses_selectionnes'])
                            messages.success(request, _("Félicitations ! Vos cours ont été activés."))
                            return redirect('subscriptions:my_subscriptions')
                        else:
                            remaining = places_restantes_apres if places_restantes_apres is not None else 0
                            messages.success(
                                request,
                                _("{} cours sélectionnés. Il vous reste {} place(s).").format(
                                    selected_courses.count(),
                                    remaining
                                )
                            )
                            return redirect('subscriptions:select_courses', pk=subscription.pk)

                except Exception as e:
                    messages.error(request, _("Erreur lors de la sélection des cours: {}").format(str(e)))
    else:
        form = CourseSelectionForm(subscription=subscription)

    return render(request, 'subscriptions/select_courses.html', {
        'form': form,
        'subscription': subscription,
        'places_restantes': places_restantes,
        'max_courses': subscription.plan.max_courses,
        'deja_selectionnes': subscription.get_courses_deja_selectionnes(),
    })


@user_passes_test(lambda u: u.is_staff)
def admin_pending(request):
    pending = Subscription.objects.filter(statut='pending').select_related('utilisateur', 'plan')
    return render(request, 'subscriptions/admin_pending.html', {'pending': pending})


# ===== VIEW VALIDATION ADMIN =====
@user_passes_test(lambda u: u.is_staff)
def admin_verify_subscription(request, pk):
    """Admin verifye epi aktive abònman an."""
    subscription = get_object_or_404(Subscription, pk=pk)

    if subscription.statut == 'active':
        messages.info(request, _("Cet abonnement est déjà actif."))
        return redirect('subscriptions:admin_pending')

    subscription.statut = 'active'
    subscription.date_debut = timezone.now()
    subscription.date_fin = timezone.now() + timezone.timedelta(days=subscription.plan.duree_jours)
    subscription.date_verification = timezone.now()
    subscription.verifie_par = request.user
    subscription.save()

    # ===== NOUVO WORKFLOW: Si max_courses > 0 =====
    try:
        if subscription.plan.max_courses > 0:
            messages.success(request, _("Abonnement activé. L'utilisateur doit maintenant choisir ses cours."))
            return redirect('subscriptions:admin_pending')
    except AttributeError:
        pass

    # ===== ANSYEN WORKFLOW: Si max_courses == 0 oswa pa egziste =====
    for cours in subscription.plan.cours.all():
        SubscriptionAccess.objects.get_or_create(
            subscription=subscription,
            cours=cours,
            defaults={'date_expiration': subscription.date_fin}
        )

    try:
        subscription.courses_selectionnes = True
        subscription.save(update_fields=['courses_selectionnes'])
    except:
        pass

    messages.success(request, _("Abonnement activé et accès créés."))
    return redirect('subscriptions:admin_pending')