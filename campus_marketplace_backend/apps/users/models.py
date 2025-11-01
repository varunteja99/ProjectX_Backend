import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('deleted', 'Deleted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    
    campus = models.ForeignKey(
        'marketplace.Campus',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES,
        default='active'
    )
    
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )
    total_reviews = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['campus']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def update_rating(self):
        """Update average rating from reviews"""
        from apps.reviews.models import Review
        reviews = Review.objects.filter(reviewee=self)
        if reviews.exists():
            self.total_reviews = reviews.count()
            self.average_rating = reviews.aggregate(
                models.Avg('rating')
            )['rating__avg']
            self.save()