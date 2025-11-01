from rest_framework import serializers
from .models import User
from apps.marketplace.models import Campus


class CampusSerializer(serializers.ModelSerializer):
    """Simplified campus info for user serializer"""
    class Meta:
        model = Campus
        fields = ['id', 'name', 'email_domain']


class UserSerializer(serializers.ModelSerializer):
    """Full user details"""
    campus = CampusSerializer(read_only=True)
    campus_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'profile_picture_url', 'student_id',
            'campus', 'campus_id', 'is_verified', 'is_active',
            'account_status', 'average_rating', 'total_reviews',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'average_rating', 'total_reviews', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'campus_id'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def validate_email(self, value):
        """Validate university email"""
        email_domain = '@' + value.split('@')[-1]
        if not Campus.objects.filter(email_domain=email_domain).exists():
            raise serializers.ValidationError(
                "Please use a valid university email address"
            )
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Get campus from email domain
        email_domain = '@' + validated_data['email'].split('@')[-1]
        campus = Campus.objects.get(email_domain=email_domain)
        validated_data['campus'] = campus
        
        user = User.objects.create_user(**validated_data, password=password)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile with limited info"""
    campus = CampusSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'profile_picture_url', 'campus', 'average_rating',
            'total_reviews', 'created_at'
        ]
        read_only_fields = fields