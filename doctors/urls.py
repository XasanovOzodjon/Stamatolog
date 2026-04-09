from django.urls import path
from . import views
from reviews.views import ReviewListCreateView

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('<int:doctor_id>/reviews/', ReviewListCreateView.as_view(), name='doctor-reviews'),
]
