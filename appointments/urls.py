from django.urls import path
from . import views

urlpatterns = [
    path('available-slots/', views.AvailableSlotsView.as_view(), name='available-slots'),
    path('available-doctors/', views.AvailableDoctorsView.as_view(), name='available-doctors'),
    path('', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
]
