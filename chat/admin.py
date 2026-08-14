from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'course', 'created_by', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'contenu_preview', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'room__type')

    def contenu_preview(self, obj):
        return obj.contenu[:50]
    contenu_preview.short_description = "Contenu"
