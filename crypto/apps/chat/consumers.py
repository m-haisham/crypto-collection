import json
import uuid
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    alias: str
    room_name: str
    room_group_name: str
    user_id: str

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        params = parse_qs(self.scope['query_string'].decode())
        self.alias = params.get('alias').pop()
        self.user_id = uuid.uuid4().hex

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
    async def receive(self, text_data=None, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'id': uuid.uuid4().hex,
                'type': 'chat_message',
                'text': message,
                'alias': self.alias,
                'user_id': self.user_id,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'text': event['text'],
            'alias': event['alias'],
            'is_self': self.user_id == event['user_id'],
        }))
