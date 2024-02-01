import json
from uuid import UUID
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessages, Conversation,Message
from django.contrib.auth.models import User
from .serializers import MessageSerializer   


class StartConnection(JsonWebsocketConsumer) :
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
    
    def connect(self):
        print("Connected!")
        self.room_name = "home"
        self.accept()
        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected initially!",
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)


class UUIDEncoder(json.JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj, UUID) :
            # returns the value of uuid if it is a uuid object
            return obj.hex
        return json.JSONDecodeError.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)



    def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            return

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
        self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)

        async_to_sync(self.channel_layer.group_add)(
        self.conversation_name,
        self.channel_name,
    )
    
        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

        messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
        self.send_json({
            "type": "last_50_messages",
            "messages": MessageSerializer(messages, many=True).data,
        })

    def disconnect(self, close_code):
        return
    
       
        
    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            message = Message.objects.create(
            from_user=self.user,
            to_user=self.get_receiver(),
            content=content["message"],
            conversation=self.conversation
            )

            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.username,
                    "message": MessageSerializer(message).data,
                },
)
        
        return super().receive_json(content, **kwargs)
    
    def get_receiver(self) :
        usernames = self.conversation_name.split("__")
        for username in usernames :
            if username != self.user.username :
                # reciever
                return User.objects.get(username=username)
    
    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)

# Receive message from WebSocket
    # def receive(self, text_data):
    #     data = json.loads(text_data)
    #     self.commands[data['command']](self, data)

    # def send_chat_message(self, message):
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name, {"type": "chat_message", "message": message}
    #     )

    # def send_message(self, message):
    #     self.send(text_data=json.dumps(message))

    #     # Receive message from room group
    # def chat_message(self, event):
    #     message = event["message"]

    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps(message))
