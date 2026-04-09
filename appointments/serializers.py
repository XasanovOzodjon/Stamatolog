from rest_framework import serializers
from django.utils import timezone
from datetime import date as date_type
from .models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    serviceId = serializers.IntegerField(source='service_id')
    doctorId = serializers.IntegerField(source='doctor_id')
    patientName = serializers.CharField(source='patient_name')
    patientPhone = serializers.CharField(source='patient_phone')
    patientEmail = serializers.EmailField(source='patient_email', required=False, allow_null=True)

    class Meta:
        model = Appointment
        fields = [
            'serviceId', 'date', 'time', 'doctorId',
            'patientName', 'patientPhone', 'patientEmail', 'notes'
        ]

    def validate_date(self, value):
        if value < date_type.today():
            raise serializers.ValidationError("Sana o'tgan bo'lmasligi kerak")
        return value

    def validate_patientPhone(self, value):
        import re
        if not re.match(r'^\+998\d{9}$', value):
            raise serializers.ValidationError("Telefon raqam noto'g'ri (+998XXXXXXXXX)")
        return value

    def validate(self, attrs):
        doctor_id = attrs.get('doctor_id')
        date = attrs.get('date')
        time = attrs.get('time')

        if doctor_id and date and time:
            conflict = Appointment.objects.filter(
                doctor_id=doctor_id, date=date, time=time
            ).exclude(status='cancelled')
            if conflict.exists():
                raise serializers.ValidationError(
                    {"time": "Tanlangan vaqt allaqachon band"}
                )
        return attrs


class AppointmentResponseSerializer(serializers.ModelSerializer):
    serviceId = serializers.IntegerField(source='service_id')
    serviceName = serializers.CharField(source='service.name')
    doctorId = serializers.IntegerField(source='doctor_id')
    doctorName = serializers.CharField(source='doctor.name')
    patientName = serializers.CharField(source='patient_name')
    patientPhone = serializers.CharField(source='patient_phone')
    patientEmail = serializers.EmailField(source='patient_email')
    createdAt = serializers.DateTimeField(source='created_at')
    time = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Appointment
        fields = [
            'id', 'serviceId', 'serviceName', 'date', 'time',
            'doctorId', 'doctorName', 'patientName', 'patientPhone',
            'patientEmail', 'notes', 'status', 'createdAt'
        ]
