from django.urls import path
from . import views

urlpatterns = [
    path('', views.GalleryListView.as_view(), name='gallery-list'),
    path('categories/', views.GalleryCategoriesView.as_view(), name='gallery-categories'),
]
