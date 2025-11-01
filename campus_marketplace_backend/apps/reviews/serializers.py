from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)
    reviewee = UserProfileSerializer(read_only=True)
    
    transaction_id = serializers.UUIDField(write_only=True)
    reviewee_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'transaction_id', 'reviewer', 'reviewee', 'reviewee_id',
            'rating', 'review_text', 'is_buyer_review', 'is_flagged',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'is_flagged', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value