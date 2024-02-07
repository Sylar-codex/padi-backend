from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinLengthValidator
from datetime import datetime
import uuid


class ChatMessages(models.Model):
    user = models.CharField(max_length=12)
    content = models.TextField(
        validators=[
            MinLengthValidator(
                1, 'the field must contain at least 1 characters')
        ])
    timestamp = models.DateTimeField(default=datetime.now)

    def get_last_10_messages(self):
        return ChatMessages.objects.order_by("-timestamp").all()[:10]
    

class Conversation(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(User, blank=True)

    def get_online_count(self) :
        return self.online.count()
    
    def join(self,user) :
        self.online.add(user)
        self.save()

    def leave(self,user) :
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"


class Message(models.Model) :
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_from_me")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_to_me")
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    



