from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', read_only=True)
    doctorId = serializers.IntegerField(source='doctor_id', read_only=True)
    patientName = serializers.CharField(source='patient_name')

    class Meta:
        model = Review
        fields = ['id', 'doctorId', 'patientName', 'rating', 'comment', 'date']
        read_only_fields = ['id', 'doctorId', 'date']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating 1 dan 5 gacha bo'lishi kerak")
        return value

    def validate_comment(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Comment kamida 10 ta belgidan iborat bo'lishi kerak"
            )
        return value
