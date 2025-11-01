from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # Safety endpoints will go here
]

router = DefaultRouter()
# router.register(r'flagged-content', views.FlaggedContentViewSet)
# router.register(r'disputes', views.DisputeViewSet)
# router.register(r'notifications', views.NotificationViewSet)

urlpatterns += router.urls