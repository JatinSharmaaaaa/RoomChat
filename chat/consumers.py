import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user_id = text_data_json.get('user_id')
        room_name = text_data_json.get('room_name')

    # Save the message to the database
        await self.save_message(user_id=user_id, room_id=self.room_name, message=message)

    # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user_id  # Or get the username here if needed
            }
         )


        
    async def chat_message(self, event):
        message = event['message']
        user = event['user']  # Get the user data

    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': user
    }))


    @database_sync_to_async
    def save_message(self, user_id, room_id, message):
        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_id)
        Message.objects.create(user=user, room=room, content=message)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

