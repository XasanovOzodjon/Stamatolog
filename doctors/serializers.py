from rest_framework import serializers
from .models import Doctor


class DoctorListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialty', 'experience', 'education',
            'description', 'image', 'rating', 'patients',
            'languages', 'work_schedule',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class DoctorAvailableSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'experience', 'image', 'rating']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
