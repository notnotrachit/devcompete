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
        # get the contest
        self.contest = Contest.objects.get(pk=1)

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
            },
        )

    def chat_msg(self, event):
        self.send(text_data=event["code"])