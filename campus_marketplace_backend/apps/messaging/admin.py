from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant_1', 'participant_2', 'listing', 'last_message_at']
    search_fields = ['participant_1__username', 'participant_2__username']
    list_filter = ['created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'conversation', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'message_text']