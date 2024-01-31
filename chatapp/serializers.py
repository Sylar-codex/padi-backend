from rest_framework import serializers
from .models import Message, Conversation
from account.serializers import UserSerializer
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer) :
    from_user= serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta :
        model = Message

        fields = "__all__"

    def get_conversation(self, obj) :
        return str(obj.conversation.id)
    
    def get_from_user(self, obj) :
        return UserSerializer(obj.from_user).data
    
    def get_to_user(self,obj) :
        return UserSerializer(obj.to_user).data
    

class ConversationSerializer(serializers.ModelSerializer) :
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta :
        model = Conversation
        ffields = ("id", "name", "other_user", "last_message")
    
    def get_last_message(self, obj) :
        messages = obj.messages.all().order_by("-timestamp")

        if not messages.exist() :
            return None
        message = messages[0]
        return MessageSerializer(message).data
    
    def get_other_user(self, obj) :
        usernames = obj.name.split("__")

        context = {}

        for username in usernames :

            # other participant
            other_user = User.objects.get(username=username)
            return UserSerializer(other_user, context=context).data 
