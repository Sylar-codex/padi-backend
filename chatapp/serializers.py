from rest_framework import serializers
from .models import Message
from account.serializers import UserSerializer


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