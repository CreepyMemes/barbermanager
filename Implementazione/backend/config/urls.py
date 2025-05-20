from django.contrib import admin
from django.conf import settings
from django.urls import path, include

# Main project's api endpoints
urlpatterns = [
    path('api/', include('api.urls')),
]

# Add admin dashboard only in dev environment
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]