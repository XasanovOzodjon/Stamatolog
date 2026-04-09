from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime, date as date_type, time as time_type, timedelta
from doctors.models import Doctor
from doctors.serializers import DoctorAvailableSerializer
from .models import Appointment
from .serializers import AppointmentCreateSerializer, AppointmentResponseSerializer
from .servise import send_telegram_notification

def generate_time_slots(start_hour=9, end_hour=18, interval_minutes=30):
    """09:00 dan 18:00 gacha 30 daqiqalik vaqt slotlari"""
    slots = []
    current = datetime.combine(date_type.today(), time_type(start_hour, 0))
    end = datetime.combine(date_type.today(), time_type(end_hour, 0))
    while current < end:
        slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=interval_minutes)
    return slots


class AvailableSlotsView(APIView):
    """GET /api/v1/appointments/available-slots/"""

    def get(self, request):
        service_id = request.query_params.get('serviceId')
        date_str = request.query_params.get('date')
        doctor_id = request.query_params.get('doctorId')

        if not service_id or not date_str:
            return Response(
                {"success": False, "error": "serviceId va date majburiy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"success": False, "error": "Sana noto'g'ri formatda (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        doctors = Doctor.objects.filter(is_available=True)
        if doctor_id:
            doctors = doctors.filter(pk=doctor_id)

        all_slots = generate_time_slots()
        result_slots = []

        for slot_time in all_slots:
            time_obj = datetime.strptime(slot_time, '%H:%M').time()
            booked_doctor_ids = set(
                Appointment.objects.filter(
                    date=query_date,
                    time=time_obj,
                ).exclude(status='cancelled').values_list('doctor_id', flat=True)
            )
            available_doctor_ids = [
                d.id for d in doctors if d.id not in booked_doctor_ids
            ]
            result_slots.append({
                "time": slot_time,
                "available": len(available_doctor_ids) > 0,
                "doctorIds": available_doctor_ids,
            })

        return Response({
            "success": True,
            "data": {"date": date_str, "slots": result_slots}
        })


class AvailableDoctorsView(APIView):
    """GET /api/v1/appointments/available-doctors/"""

    def get(self, request):
        service_id = request.query_params.get('serviceId')
        date_str = request.query_params.get('date')
        time_str = request.query_params.get('time')

        if not all([service_id, date_str, time_str]):
            return Response(
                {"success": False, "error": "serviceId, date va time majburiy"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query_time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return Response(
                {"success": False, "error": "Sana yoki vaqt formati noto'g'ri"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booked_ids = Appointment.objects.filter(
            date=query_date, time=query_time
        ).exclude(status='cancelled').values_list('doctor_id', flat=True)

        available_doctors = Doctor.objects.filter(
            is_available=True
        ).exclude(id__in=booked_ids)

        serializer = DoctorAvailableSerializer(
            available_doctors, many=True, context={'request': request}
        )
        return Response({"success": True, "data": serializer.data})


class AppointmentCreateView(APIView):
    """POST /api/v1/appointments/"""

    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Conflict tekshirish
            data = serializer.validated_data
            conflict = Appointment.objects.filter(
                doctor_id=data['doctor_id'],
                date=data['date'],
                time=data['time'],
            ).exclude(status='cancelled')

            if conflict.exists():
                return Response(
                    {"success": False, "error": "Tanlangan vaqt allaqachon band"},
                    status=status.HTTP_409_CONFLICT
                )

            appointment = serializer.save()
            response_serializer = AppointmentResponseSerializer(appointment)
            send_telegram_notification(appointment)
            return Response(
                {"success": True, "data": response_serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"success": False, "error": "Validation error", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class AppointmentDetailView(APIView):
    """GET /api/v1/appointments/:id/"""

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        serializer = AppointmentResponseSerializer(appointment)
        return Response({"success": True, "data": serializer.data})

    def delete(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if appointment.status == 'cancelled':
            return Response(
                {"success": False, "error": "Appointment allaqachon bekor qilingan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = 'cancelled'
        appointment.save(update_fields=['status'])
        return Response({"success": True, "message": "Appointment bekor qilindi"})
