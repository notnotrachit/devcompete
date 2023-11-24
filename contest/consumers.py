import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Contest


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.contest = None

    def connect(self):
        self.room_name = str(self.scope['url_route']['kwargs']['room_name'])
        self.contest = Contest.objects.get(pk=int(self.room_name))

        # get the user
        user = self.scope['user']
        if user != self.contest.player1 and user != self.contest.player2:
            self.close()
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name,
        )

    # def disconnect(self, close_code):
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_name,
    #         self.contest.name,
    #     )
    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        code = text_data_json['code']

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_msg',
                'code': code,
                'user': self.scope['user'].username,
                'player_number': 1 if self.scope['user'] == self.contest.player1 else 2,
            },
        )

    def chat_msg(self, event):
        self.send(text_data=json.dumps({
            'code': event['code'],
            'user': event['user'],
            'player_number': event['player_number'],
        }))