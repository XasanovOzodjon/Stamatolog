from django.contrib import admin
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active']
