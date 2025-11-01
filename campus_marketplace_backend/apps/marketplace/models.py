import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta


class Campus(models.Model):
    """University/Campus information"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=100, unique=True, help_text="e.g., @pfw.edu")
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='USA')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'campuses'
        verbose_name_plural = 'Campuses'
        indexes = [
            models.Index(fields=['email_domain']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Item categories"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    icon_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    """Item listings"""
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
        ('deleted', 'Deleted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='listings'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=255, blank=True)
    
    view_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_negotiable = models.BooleanField(default=True)
    
    expires_at = models.DateTimeField(null=True, blank=True)
    sold_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller']),
            models.Index(fields=['category']),
            models.Index(fields=['campus']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.conf import settings
            self.expires_at = timezone.now() + timedelta(
                days=settings.LISTING_EXPIRY_DAYS
            )
        super().save(*args, **kwargs)
    
    def increment_view_count(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class ListingImage(models.Model):
    """Listing images"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image_url = models.URLField()
    display_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'listing_images'
        ordering = ['display_order']
        indexes = [
            models.Index(fields=['listing', 'display_order']),
        ]
    
    def __str__(self):
        return f"Image for {self.listing.title}"


class Textbook(models.Model):
    """Textbook-specific information"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE,
        related_name='textbook'
    )
    
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    
    course_code = models.CharField(max_length=50, blank=True)
    course_name = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_required = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'textbooks'
        indexes = [
            models.Index(fields=['isbn_13']),
            models.Index(fields=['isbn_10']),
            models.Index(fields=['course_code']),
        ]
    
    def __str__(self):
        return self.title


class Wishlist(models.Model):
    """User wishlist"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'wishlists'
        unique_together = ['user', 'listing']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['listing']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class SavedSearch(models.Model):
    """Saved search queries"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='saved_searches'
    )
    search_name = models.CharField(max_length=255)
    search_query = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    min_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    max_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    condition = models.CharField(max_length=20, blank=True)
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    notification_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'saved_searches'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.search_name}"