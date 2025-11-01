from rest_framework import serializers
from .models import Conversation, Message
from apps.users.serializers import UserProfileSerializer
from apps.marketplace.serializers import ListingListSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)
    receiver = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'receiver', 'message_text',
            'is_read', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'is_read', 'created_at', 'read_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_text', 'receiver_id']
    
    receiver_id = serializers.UUIDField(write_only=True)


class ConversationSerializer(serializers.ModelSerializer):
    participant_1 = UserProfileSerializer(read_only=True)
    participant_2 = UserProfileSerializer(read_only=True)
    listing = ListingListSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participant_1', 'participant_2', 'listing',
            'last_message', 'unread_count', 'last_message_at', 'created_at'
        ]
        read_only_fields = fields
    
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by('-created_at').first()
        if last_msg:
            return {
                'text': last_msg.message_text,
                'sender': last_msg.sender.username,
                'created_at': last_msg.created_at
            }
        return None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(receiver=user, is_read=False).count()