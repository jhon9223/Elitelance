from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    # Core Landing Page
    path('', include('core.urls')),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Dashboard
    path('dashboard/', include('dashboard.urls')),

    # Jobs System
    path('jobs/', include('jobs.urls')),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
