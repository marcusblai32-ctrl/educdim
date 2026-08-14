from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils import timezone
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'birth_year')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

@admin.action(description="Envoyer notification aux utilisateurs inactifs")
def send_inactive_notification(modeladmin, request, queryset):
    from .management.commands.check_inactive_users import Command
    cmd = Command()
    count = 0
    for user in queryset:
        if user.is_inactive(90) and not user.notification_sent:
            cmd.send_notification(user, 90, 120)
            user.notification_sent = True
            user.notification_date = timezone.now()
            user.save()
            count += 1
    modeladmin.message_user(request, f"Notifications envoyées à {count} utilisateurs")

@admin.action(description="Marquer pour suppression")
def mark_for_deletion(modeladmin, request, queryset):
    from django.utils import timezone
    import datetime
    count = 0
    for user in queryset:
        if user.is_inactive(90) and user.notification_sent:
            user.delete_scheduled = True
            user.delete_date = timezone.now() + datetime.timedelta(days=30)
            user.save()
            count += 1
    modeladmin.message_user(request, f"{count} utilisateurs marqués pour suppression")

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_activity')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'notification_sent', 'delete_scheduled')
    search_fields = ('email', 'first_name', 'last_name', 'user_id')
    ordering = ('email',)
    actions = [send_inactive_notification, mark_for_deletion]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Infos personnelles', {'fields': ('first_name', 'last_name', 'birth_year', 'user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login',)}),
        ('Activité', {'fields': ('last_activity', 'notification_sent', 'notification_date', 'delete_scheduled', 'delete_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'birth_year', 'password1', 'password2')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
