from rest_framework import serializers
from .models import Campus, Category, Listing, ListingImage, Textbook, Wishlist, SavedSearch


class CampusSerializer(serializers.ModelSerializer):
    """Campus serializer - single source of truth"""
    class Meta:
        model = Campus
        fields = ['id', 'name', 'email_domain', 'city', 'state', 'zip_code', 'is_active']
        read_only_fields = ['id']
        ref_name = 'MarketplaceCampus'  # Explicit ref_name for Swagger


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'icon_url', 
                  'display_order', 'is_active', 'subcategories']
        read_only_fields = ['id']
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
        return []


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image_url', 'display_order', 'is_primary']
        read_only_fields = ['id']


class TextbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textbook
        fields = [
            'id', 'isbn_10', 'isbn_13', 'title', 'author', 'edition',
            'publisher', 'publication_year', 'course_code', 'course_name',
            'department', 'is_required'
        ]
        read_only_fields = ['id']


# Import UserProfileSerializer locally to avoid circular import
class ListingSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    campus = CampusSerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    textbook = TextbookSerializer(read_only=True)
    
    # Write-only fields for creating/updating
    category_id = serializers.UUIDField(write_only=True)
    campus_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Listing
        fields = [
            'id', 'seller', 'category', 'category_id', 'campus', 'campus_id',
            'title', 'description', 'price', 'condition', 'status', 'location',
            'view_count', 'is_featured', 'is_negotiable', 'images', 'textbook',
            'expires_at', 'sold_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'seller', 'view_count', 'sold_at', 'created_at', 'updated_at']
    
    def get_seller(self, obj):
        from apps.users.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.seller).data
    
    def create(self, validated_data):
        # Set seller from request user
        validated_data['seller'] = self.context['request'].user
        
        # Set campus to user's campus if not provided
        if 'campus_id' not in validated_data:
            validated_data['campus_id'] = self.context['request'].user.campus_id
        
        return super().create(validated_data)


class ListingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating listings"""
    images = ListingImageSerializer(many=True, required=False)
    textbook = TextbookSerializer(required=False)
    category_id = serializers.UUIDField(write_only=True)
    campus_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Listing
        fields = [
            'category_id', 'campus_id', 'title', 'description', 'price', 'condition',
            'location', 'is_negotiable', 'images', 'textbook'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        textbook_data = validated_data.pop('textbook', None)

        # Set seller and campus_id (if not provided)
        validated_data['seller'] = self.context['request'].user
        if 'campus_id' not in validated_data:
            validated_data['campus_id'] = self.context['request'].user.campus_id

        listing = Listing.objects.create(**validated_data)
        
        # Create images
        for image_data in images_data:
            ListingImage.objects.create(listing=listing, **image_data)
        
        # Create textbook info if provided
        if textbook_data:
            Textbook.objects.create(listing=listing, **textbook_data)
        
        return listing


class ListingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing lists"""
    seller = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'price', 'condition', 'status', 'location',
            'seller', 'primary_image', 'created_at'
        ]
    
    def get_seller(self, obj):
        from apps.users.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.seller).data
    
    def get_primary_image(self, obj):
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image:
            return image.image_url
        return None


class WishlistSerializer(serializers.ModelSerializer):
    listing = ListingListSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'listing', 'listing_id', 'created_at']
        read_only_fields = ['id', 'created_at']


class SavedSearchSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    campus = CampusSerializer(read_only=True)
    campus_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SavedSearch
        fields = [
            'id', 'search_name', 'search_query', 'category', 'category_id',
            'min_price', 'max_price', 'condition', 'campus', 'campus_id',
            'is_active', 'notification_enabled', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']