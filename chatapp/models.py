from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinLengthValidator


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
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)



