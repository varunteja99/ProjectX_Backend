from django.urls import path
from rest_framework.routers import DefaultRouter

# We'll add views later
urlpatterns = [
    # Listing endpoints will go here
]

router = DefaultRouter()
# router.register(r'listings', views.ListingViewSet)
# router.register(r'categories', views.CategoryViewSet)
# router.register(r'campuses', views.CampusViewSet)

urlpatterns += router.urls