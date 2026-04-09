from rest_framework import serializers
from .models import GalleryItem


class GalleryItemSerializer(serializers.ModelSerializer):
    beforeImage = serializers.SerializerMethodField()
    afterImage = serializers.SerializerMethodField()

    class Meta:
        model = GalleryItem
        fields = ['id', 'category', 'beforeImage', 'afterImage', 'description']

    def get_beforeImage(self, obj):
        request = self.context.get('request')
        if obj.before_image and request:
            return request.build_absolute_uri(obj.before_image.url)
        return None

    def get_afterImage(self, obj):
        request = self.context.get('request')
        if obj.after_image and request:
            return request.build_absolute_uri(obj.after_image.url)
        return None
