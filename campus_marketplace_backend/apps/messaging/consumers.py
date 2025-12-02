import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Verify user is participant
        if not await self.is_participant():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        
        # Save message to database
        message = await self.save_message(message_text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': str(self.scope['user'].id),
                'sender_username': self.scope['user'].username,
                'created_at': message.created_at.isoformat(),
                'id': str(message.id)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'created_at': event['created_at'],
            'id': event['id']
        }))

    @database_sync_to_async
    def is_participant(self):
        from .models import Conversation
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
            return conversation.participant_1 == user or conversation.participant_2 == user
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, message_text):
        from .models import Conversation, Message
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.scope['user'],
            receiver=conversation.get_other_participant(self.scope['user']),
            message_text=message_text
        )
