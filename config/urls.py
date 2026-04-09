from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('doctors/', include('doctors.urls')),
        path('services/', include('services.urls')),
        path('appointments/', include('appointments.urls')),
        path('gallery/', include('gallery.urls')),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
