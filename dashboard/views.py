from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import AdminDashboard

@staff_member_required
def admin_dashboard(request):
    """Vue dashboard admin"""
    dashboard, created = AdminDashboard.objects.get_or_create(id=1)
    dashboard.update_stats()

    return render(request, 'admin/dashboard.html', {
        'dashboard': dashboard,
        'title': 'Tableau de bord'
    })
