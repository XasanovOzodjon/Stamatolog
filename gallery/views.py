from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GalleryItem
from .serializers import GalleryItemSerializer


class GalleryListView(APIView):
    """GET /api/v1/gallery/"""

    def get(self, request):
        items = GalleryItem.objects.filter(is_active=True)

        category = request.query_params.get('category')
        if category:
            items = items.filter(category__icontains=category)

        serializer = GalleryItemSerializer(items, many=True, context={'request': request})
        return Response({"success": True, "data": serializer.data})


class GalleryCategoriesView(APIView):
    """GET /api/v1/gallery/categories/"""

    def get(self, request):
        categories = (
            GalleryItem.objects.filter(is_active=True)
            .values_list('category', flat=True)
            .distinct()
        )
        return Response({"success": True, "data": list(categories)})
