from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'service', 'date', 'time', 'status']
    list_filter = ['status', 'date', 'doctor']
    search_fields = ['patient_name', 'patient_phone']
    list_editable = ['status']
    ordering = ['-date', '-time']
