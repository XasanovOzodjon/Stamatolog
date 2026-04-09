from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'rating', 'created_at']
    list_filter = ['rating', 'doctor']
    search_fields = ['patient_name']
    ordering = ['-created_at']
