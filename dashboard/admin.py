from django.contrib import admin
from .models import AdminDashboard

@admin.register(AdminDashboard)
class AdminDashboardAdmin(admin.ModelAdmin):
    list_display = ('last_updated', 'total_users', 'total_courses', 'total_revenue', 'active_subscriptions')
    readonly_fields = ('last_updated',)

    fieldsets = (
        ('📊 Utilisateurs', {'fields': ('total_users', 'new_users_today', 'active_users_today', 'total_teachers')}),
        ('📚 Contenu', {'fields': ('total_courses', 'total_lessons', 'total_quizzes', 'total_enrollments')}),
        ('💰 Revenus', {'fields': ('total_revenue', 'revenue_this_month', 'revenue_this_week', 'pending_payments')}),
        ('📈 Abonnements', {'fields': ('active_subscriptions', 'growth_percentage')}),
        ('🔄 Dernière mise à jour', {'fields': ('last_updated',)}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
