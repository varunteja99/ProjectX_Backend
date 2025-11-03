from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampusViewSet, CategoryViewSet, ListingViewSet,
    WishlistViewSet, SavedSearchViewSet
)

router = DefaultRouter()
router.register(r'campuses', CampusViewSet, basename='campus')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'saved-searches', SavedSearchViewSet, basename='saved-search')

urlpatterns = [
    path('', include(router.urls)),
]