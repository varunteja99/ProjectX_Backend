from rest_framework import serializers
from .models import Offer, Transaction, MeetingLocation
from apps.users.serializers import UserProfileSerializer
from apps.marketplace.serializers import ListingListSerializer


class OfferSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)
    listing = ListingListSerializer(read_only=True)
    
    listing_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Offer
        fields = [
            'id', 'listing', 'listing_id', 'buyer', 'seller',
            'offer_amount', 'message', 'status', 'parent_offer',
            'expires_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'buyer', 'seller', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        listing_id = validated_data.pop('listing_id')
        from apps.marketplace.models import Listing
        
        listing = Listing.objects.get(id=listing_id)
        validated_data['listing'] = listing
        validated_data['buyer'] = self.context['request'].user
        validated_data['seller'] = listing.seller
        
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)
    listing = ListingListSerializer(read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'listing', 'buyer', 'seller', 'offer', 'final_price',
            'status', 'meeting_location', 'meeting_time', 'payment_method',
            'notes', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'buyer', 'seller', 'completed_at', 'created_at', 'updated_at']


class MeetingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingLocation
        fields = [
            'id', 'campus', 'name', 'description', 'location_type',
            'address', 'building', 'room_number', 'hours_of_operation',
            'is_verified', 'is_active'
        ]
        read_only_fields = ['id']