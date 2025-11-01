from django.contrib import admin
from .models import Offer, Transaction, MeetingLocation


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['listing', 'buyer', 'seller', 'offer_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['listing__title', 'buyer__username', 'seller__username']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['listing', 'buyer', 'seller', 'final_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['listing__title', 'buyer__username', 'seller__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MeetingLocation)
class MeetingLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'campus', 'location_type', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active', 'location_type', 'campus']
    search_fields = ['name', 'building']