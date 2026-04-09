from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'experience', 'rating', 'is_available']
    list_filter = ['specialty', 'is_available']
    search_fields = ['name', 'specialty']
