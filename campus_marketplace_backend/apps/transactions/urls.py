from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # Transaction endpoints will go here
]

router = DefaultRouter()
# router.register(r'offers', views.OfferViewSet)
# router.register(r'transactions', views.TransactionViewSet)

urlpatterns += router.urls