from django.urls import path
from rest_framework.routers import DefaultRouter

# We'll add views later
urlpatterns = [
    # Authentication endpoints will go here
    # path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
]

# Router for viewsets (we'll add later)
router = DefaultRouter()
# router.register(r'profile', views.UserViewSet)

urlpatterns += router.urls