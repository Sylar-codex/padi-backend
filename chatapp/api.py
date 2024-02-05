from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from knox.auth import TokenAuthentication
from rest_framework import permissions, generics, mixins
from .models import Message
from .paginaters import MessagePagination


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
    

class MessageViewSet(GenericViewSet, mixins.ListModelMixin) :
    authentication_classes = (TokenAuthentication,)

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    
    pagination_class = MessagePagination

    def get_queryset(self) :

        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )

        return queryset
