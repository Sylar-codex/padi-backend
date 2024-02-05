# chat/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import ConversationViewSet, MessageViewSet

router = DefaultRouter()

router.register("api/conversations", ConversationViewSet)
router.register("api/messages", MessageViewSet)

urlpatterns = router.urls

