from django.contrib import admin
from .models import Advertisement, FavoriteAdvertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'creator', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(FavoriteAdvertisement)
class FavoriteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'advertisement', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'advertisement__title']