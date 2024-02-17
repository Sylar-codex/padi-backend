from rest_framework import serializers
from .models import Message, Conversation
from account.serializers import UserSerializer
from django.contrib.auth.models import User
from account.models import UserProfile
from account.serializers import UserProfileSerializer


class MessageSerializer(serializers.ModelSerializer) :
    from_user= serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()
    to_user_profile = serializers.SerializerMethodField()
    from_user_profile = serializers.SerializerMethodField()

    class Meta :
        model = Message

        fields = "__all__"

    def get_conversation(self, obj) :
        return str(obj.conversation.id)
    
    def get_from_user(self, obj) :
        return UserSerializer(obj.from_user).data
    
    def get_to_user(self,obj) :
        return UserSerializer(obj.to_user).data
    
    def get_to_user_profile(self, obj) :
        context = {}
        to_user = User.objects.get(username=obj.to_user)
        other_user_profile = UserProfile.objects.get(user=to_user)
        return UserProfileSerializer(other_user_profile, context=context).data
    
    def get_from_user_profile(self,obj) :
        context = {}
        from_user = User.objects.get(username=obj.from_user)
        other_user_profile = UserProfile.objects.get(user=from_user)
        return UserProfileSerializer(other_user_profile, context=context).data

    

class ConversationSerializer(serializers.ModelSerializer) :
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_user_profile = serializers.SerializerMethodField()

    class Meta :
        model = Conversation
        fields = ("id", "name", "other_user", "last_message", "unread_count","other_user_profile")
    
    def get_last_message(self, obj) :
        messages = obj.messages.all().order_by("-timestamp")

        if not messages.exists() :
            return None
        message = messages[0]
        return MessageSerializer(message).data
    
    def get_unread_count(self,obj) :
        context = {}
        return obj.messages.filter(to_user=self.context["user"], read=False).count()
    
    def get_other_user_profile(self,obj) :
        usernames = obj.name.split("__")
        context = {}
        for username in usernames:
            if username != self.context["user"].username :
                other_user = User.objects.get(username=username)
                other_user_profile = UserProfile.objects.get(user=other_user)
                return UserProfileSerializer(other_user_profile, context=context).data


    
    def get_other_user(self, obj) :
        usernames = obj.name.split("__")

        context = {}

        for username in usernames :
            if username != self.context["user"].username :

                # other participant
                other_user = User.objects.get(username=username)
                return UserSerializer(other_user, context=context).data 
