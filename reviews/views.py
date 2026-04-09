from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from doctors.models import Doctor
from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(APIView):
    """GET/POST /api/v1/doctors/:doctor_id/reviews/"""

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        reviews = Review.objects.filter(doctor=doctor)

        page_num = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))

        paginator = Paginator(reviews, limit)
        page = paginator.get_page(page_num)

        serializer = ReviewSerializer(page.object_list, many=True)
        return Response({
            "success": True,
            "data": {
                "reviews": serializer.data,
                "pagination": {
                    "page": page_num,
                    "limit": limit,
                    "total": paginator.count,
                    "pages": paginator.num_pages,
                }
            }
        })

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(doctor=doctor)
            # Doctor ratingini yangilash
            reviews = Review.objects.filter(doctor=doctor)
            avg = sum(r.rating for r in reviews) / reviews.count()
            doctor.rating = round(avg, 1)
            doctor.save(update_fields=['rating'])

            return Response(
                {"success": True, "data": ReviewSerializer(review).data},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"success": False, "error": "Validation error", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
