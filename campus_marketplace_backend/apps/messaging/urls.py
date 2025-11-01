from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # Messaging endpoints will go here
]

router = DefaultRouter()
# router.register(r'conversations', views.ConversationViewSet)
# router.register(r'messages', views.MessageViewSet)

urlpatterns += router.urls