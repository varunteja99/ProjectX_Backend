from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageCreateSerializer


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for conversations"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get conversations for current user"""
        user = self.request.user
        return Conversation.objects.filter(
            Q(participant_1=user) | Q(participant_2=user)
        ).select_related(
            'participant_1', 'participant_2', 'listing'
        ).prefetch_related('messages').order_by('-last_message_at')
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a conversation"""
        conversation = self.get_object()
        messages = conversation.messages.order_by('created_at')
        
        # Mark messages as read
        messages.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get messages for current user"""
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver', 'conversation')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        """Send a new message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        receiver_id = serializer.validated_data['receiver_id']
        message_text = serializer.validated_data['message_text']
        
        from apps.users.models import User
        receiver = User.objects.get(id=receiver_id)
        
        # Get or create conversation
        conversation = Conversation.objects.filter(
            (Q(participant_1=request.user) & Q(participant_2=receiver)) |
            (Q(participant_1=receiver) & Q(participant_2=request.user))
        ).first()
        
        if not conversation:
            conversation = Conversation.objects.create(
                participant_1=request.user,
                participant_2=receiver
            )
        
        # Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            receiver=receiver,
            message_text=message_text
        )
        
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread message count"""
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})