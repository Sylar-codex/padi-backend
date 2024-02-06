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
    
        self.send_json( {
            "type":"online_user_list",
            "users": [user.username for user in self.conversation.online.all()],
        }
           
        )

        async_to_sync(self.channel_layer.group_send) (
            self.conversation_name,
            {
                "type" :"user_join",
                "user":self.user.username
            }
        )

        self.conversation.online.add(self.user)

        messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
        message_count = self.conversation.messages.all().count()
        self.send_json({
            "type": "last_50_messages",
            "messages": MessageSerializer(messages, many=True).data,
            "has_more": message_count > 10,
        })

    def disconnect(self, close_code):
        if self.user.is_authenticated :
            async_to_sync(self.channel_layer.group_send) (
                self.conversation_name,
                {
                "type":"user_leave",
                "user":self.user.username
                }
                
            )
            self.conversation.online.remove(self.user)
        return super().disconnect(close_code)
    
       
        
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
            
        if message_type == "typing":

            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "typing",
                "user": self.user.username,
                "typing": content["typing"],
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
        self.send_json(event)

    def user_join(self, event) :
        self.send_json(event)
    
    def user_leave(self,event) :
        self.send_json(event)
    
    def typing(self, event):
        self.send_json(event)



class NotificationConsumer(JsonWebsocketConsumer) :
    def __init__(self, *args, **kwargs) :
        super().__init__(args, kwargs)
        self.user = None

    def connect(self) :
        self.user= self.scope["user"]
        if not self.user.is_authenticated():
            return
        
        self.accept()

        unread_count = Message.objects.filter(to_user=self.user, read=False).count()
        self.send_json(
        {
            "type": "unread_count",
            "unread_count": unread_count,
        }
    )