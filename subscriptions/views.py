from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import SubscriptionPlan, Subscription, SubscriptionAccess
from .forms import SubscriptionForm

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
    plan = get_object_or_404(SubscriptionPlan, pk=plan_pk, actif=True)

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

                for cours in plan.cours.all():
                    SubscriptionAccess.objects.create(
                        subscription=subscription,
                        cours=cours,
                        date_expiration=subscription.date_fin
                    )

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
    return render(request, 'subscriptions/detail.html', {
        'subscription': sub,
        'accesses': accesses,
    })

@user_passes_test(lambda u: u.is_staff)
def admin_pending(request):
    pending = Subscription.objects.filter(statut='pending').select_related('utilisateur', 'plan')
    return render(request, 'subscriptions/admin_pending.html', {'pending': pending})
