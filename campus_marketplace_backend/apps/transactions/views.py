from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Offer, Transaction, MeetingLocation
from .serializers import (
    OfferSerializer, TransactionSerializer, MeetingLocationSerializer
)


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for offers"""
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get offers for current user (as buyer or seller)"""
        user = self.request.user
        return Offer.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related('buyer', 'seller', 'listing').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def received(self, request):
        """Get offers received (as seller)"""
        offers = self.get_queryset().filter(seller=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get offers sent (as buyer)"""
        offers = self.get_queryset().filter(buyer=request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept an offer"""
        offer = self.get_object()
        
        if offer.seller != request.user:
            return Response(
                {'error': 'Only the seller can accept offers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if offer.status != 'pending':
            return Response(
                {'error': 'Offer is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        offer.status = 'accepted'
        offer.save()
        
        # Create transaction
        Transaction.objects.create(
            listing=offer.listing,
            buyer=offer.buyer,
            seller=offer.seller,
            offer=offer,
            final_price=offer.offer_amount,
            status='negotiating'
        )
        
        return Response({'status': 'Offer accepted'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject an offer"""
        offer = self.get_object()
        
        if offer.seller != request.user:
            return Response(
                {'error': 'Only the seller can reject offers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        offer.status = 'rejected'
        offer.save()
        
        return Response({'status': 'Offer rejected'})
    
    @action(detail=True, methods=['post'])
    def counter(self, request, pk=None):
        """Counter an offer"""
        offer = self.get_object()
        
        if offer.seller != request.user:
            return Response(
                {'error': 'Only the seller can counter offers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        counter_amount = request.data.get('offer_amount')
        if not counter_amount:
            return Response(
                {'error': 'Counter amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create counter offer
        counter_offer = Offer.objects.create(
            listing=offer.listing,
            buyer=offer.buyer,
            seller=offer.seller,
            offer_amount=counter_amount,
            message=request.data.get('message', ''),
            parent_offer=offer
        )
        
        offer.status = 'countered'
        offer.save()
        
        return Response(OfferSerializer(counter_offer).data)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get transactions for current user (as buyer or seller)"""
        user = self.request.user
        return Transaction.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related('buyer', 'seller', 'listing').order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def purchases(self, request):
        """Get purchases (as buyer)"""
        transactions = self.get_queryset().filter(buyer=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sales(self, request):
        """Get sales (as seller)"""
        transactions = self.get_queryset().filter(seller=request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark transaction as completed"""
        transaction = self.get_object()
        
        if transaction.buyer != request.user and transaction.seller != request.user:
            return Response(
                {'error': 'Only buyer or seller can complete transaction'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        transaction.status = 'completed'
        transaction.save()
        
        return Response({'status': 'Transaction completed'})


class MeetingLocationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for meeting locations"""
    serializer_class = MeetingLocationSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = MeetingLocation.objects.filter(is_active=True)
        
        campus_id = self.request.query_params.get('campus_id')
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        
        return queryset