import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessages, Conversation


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

    def fetch_messages(self, data):
        messages = ChatMessages.get_last_10_messages()
        content = {
            "messages": self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user = data['from']
        message = ChatMessages.objects.create(
            user=user, content=data['message'])

        content = {
            "command": "new_message",
            "message": self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.user,
            "content": message.content,
            "timestamp": str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_messages': new_message
    }

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

    def disconnect(self, close_code):
        return
    
       
        
    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "chat_message_echo",
                "username": content["username"],
                "message": content["message"],
            },
        )
        return super().receive_json(content, **kwargs)
    
    def chat_message_echo(self, event):
        print("echo_func",event)
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
