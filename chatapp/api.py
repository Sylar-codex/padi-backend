from .serializers import ConversationSerializer
from .models import Conversation
from rest_framework.viewsets import ModelViewSet
from knox.auth import TokenAuthentication
from rest_framework import permissions


class ConversationViewSet(ModelViewSet) :
    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = ConversationSerializer
    queryset= Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(name__contains=self.request.user.username)
        return queryset
    
    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
