from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Doctor
from .serializers import DoctorListSerializer


class DoctorListView(APIView):
    """GET /api/v1/doctors/ - Barcha doctorlar"""

    def get(self, request):
        doctors = Doctor.objects.all()

        specialty = request.query_params.get('specialty')
        if specialty:
            doctors = doctors.filter(specialty__icontains=specialty)

        available = request.query_params.get('available')
        if available is not None:
            is_available = available.lower() in ('true', '1', 'yes')
            doctors = doctors.filter(is_available=is_available)

        serializer = DoctorListSerializer(doctors, many=True, context={'request': request})
        return Response({"success": True, "data": serializer.data})


class DoctorDetailView(APIView):
    """GET /api/v1/doctors/:id/ - Bitta doctor"""

    def get(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorListSerializer(doctor, context={'request': request})
        return Response({"success": True, "data": serializer.data})
