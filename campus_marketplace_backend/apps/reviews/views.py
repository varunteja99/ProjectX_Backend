from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for reviews"""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get reviews"""
        queryset = Review.objects.select_related('reviewer', 'reviewee')
        
        # Filter by reviewee
        reviewee_id = self.request.query_params.get('reviewee_id')
        if reviewee_id:
            queryset = queryset.filter(reviewee_id=reviewee_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Create a review"""
        serializer.save(reviewer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get reviews for current user"""
        reviews = Review.objects.filter(reviewee=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def given_reviews(self, request):
        """Get reviews given by current user"""
        reviews = Review.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)