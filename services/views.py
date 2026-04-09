from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(APIView):
    """GET /api/v1/services/"""

    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServiceSerializer(services, many=True)
        return Response({"success": True, "data": serializer.data})


class ServiceDetailView(APIView):
    """GET /api/v1/services/:id/"""

    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk, is_active=True)
        serializer = ServiceSerializer(service)
        return Response({"success": True, "data": serializer.data})
