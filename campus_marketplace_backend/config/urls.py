from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Campus Marketplace API",
        default_version='v1',
        description="API documentation for Campus Marketplace",
        terms_of_service="https://www.campusmarketplace.com/terms/",
        contact=openapi.Contact(email="contact@campusmarketplace.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/marketplace/', include('apps.marketplace.urls')),
    path('api/v1/messaging/', include('apps.messaging.urls')),
    path('api/v1/transactions/', include('apps.transactions.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/safety/', include('apps.safety.urls')),
    path('api/v1/admin/', include('apps.admin_panel.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)