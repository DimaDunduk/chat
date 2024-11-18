# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chat.models import PetsPerson
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        user = self.scope['user']

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if user.is_authenticated:
            pets_person = PetsPerson.objects.get(user=user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'first_name': pets_person.first_name,
                    'last_name': pets_person.last_name,
                    'profile_image': pets_person.profile_image.url if pets_person.profile_image else None,
                }
            )

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            pets_person = PetsPerson.objects.get(user=user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'first_name': pets_person.first_name,
                    'last_name': pets_person.last_name,
                }
            )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'notification': f"{event['first_name']} {event['last_name']} has joined",
            'profile_image': event['profile_image'],
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'notification': f"{event['first_name']} {event['last_name']} has left",
        }))
