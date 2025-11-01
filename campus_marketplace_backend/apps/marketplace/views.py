from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Campus, Category, Listing, Wishlist, SavedSearch
from .serializers import (
    CampusSerializer, CategorySerializer, ListingSerializer,
    ListingCreateSerializer, ListingListSerializer, WishlistSerializer,
    SavedSearchSerializer
)


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for campuses"""
    queryset = Campus.objects.filter(is_active=True)
    serializer_class = CampusSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories"""
    queryset = Category.objects.filter(is_active=True, parent__isnull=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def subcategories(self, request, slug=None):
        """Get subcategories for a category"""
        category = self.get_object()
        subcategories = category.subcategories.filter(is_active=True)
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for listings"""
    queryset = Listing.objects.filter(status='active').select_related(
        'seller', 'category', 'campus'
    ).prefetch_related('images')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'campus', 'condition', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'view_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ListingCreateSerializer
        elif self.action == 'list':
            return ListingListSerializer
        return ListingSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        """Get listing details and increment view count"""
        listing = self.get_object()
        listing.increment_view_count()
        serializer = self.get_serializer(listing)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get current user's listings"""
        listings = self.queryset.filter(seller=request.user)
        serializer = ListingListSerializer(listings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_sold(self, request, pk=None):
        """Mark listing as sold"""
        listing = self.get_object()
        
        if listing.seller != request.user:
            return Response(
                {'error': 'Only the seller can mark as sold'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        listing.status = 'sold'
        listing.save()
        
        return Response({'status': 'Listing marked as sold'})


class WishlistViewSet(viewsets.ModelViewSet):
    """ViewSet for wishlist"""
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SavedSearchViewSet(viewsets.ModelViewSet):
    """ViewSet for saved searches"""
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)