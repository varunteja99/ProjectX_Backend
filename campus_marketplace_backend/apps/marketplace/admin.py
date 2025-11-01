from django.contrib import admin
from .models import Campus, Category, Listing, ListingImage, Textbook, Wishlist, SavedSearch


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'email_domain', 'city', 'state', 'is_active']
    list_filter = ['is_active', 'state']
    search_fields = ['name', 'email_domain', 'city']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'display_order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'condition', 'status', 'campus', 'created_at']
    list_filter = ['status', 'condition', 'campus', 'category']
    search_fields = ['title', 'description', 'seller__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['view_count', 'created_at', 'updated_at']


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'display_order', 'is_primary', 'created_at']
    list_filter = ['is_primary']


@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn_13', 'author', 'course_code', 'is_required']
    search_fields = ['title', 'isbn_13', 'isbn_10', 'course_code', 'author']
    list_filter = ['is_required', 'department']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'listing__title']


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_name', 'category', 'is_active', 'notification_enabled']
    list_filter = ['is_active', 'notification_enabled', 'category']
    search_fields = ['user__username', 'search_name']