from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FlaggedContentViewSet, NotificationViewSet, StudyMaterialViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register(r'flagged-content', FlaggedContentViewSet, basename='flagged-content')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'study-materials', StudyMaterialViewSet, basename='study-material')

urlpatterns = [
    path('', include(router.urls)),
]