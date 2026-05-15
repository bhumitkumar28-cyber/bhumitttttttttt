from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public_app.urls')),
    path('donor/', include('donor_app.urls')),
    path('requester/', include('requester_app.urls')),
    path('hospital-admin/', include('hospital_admin_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)