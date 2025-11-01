from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # Admin panel endpoints will go here
]

router = DefaultRouter()
# router.register(r'activity-logs', views.ActivityLogViewSet)
# router.register(r'system-settings', views.SystemSettingViewSet)

urlpatterns += router.urls