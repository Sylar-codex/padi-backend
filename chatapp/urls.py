# chat/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from .api import ConversationViewSet

router = DefaultRouter()

router.register("api/conversations", ConversationViewSet)

urlpatterns = router.urls

