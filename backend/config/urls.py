from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from api.views import SpectacularJSONAPIView, SpectacularSwaggerView


# Main project's api endpoints
urlpatterns = [
    # Backend API endpoints
    path('api/', include('api.urls')),

    # OpenAPI JSON schema
    path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),

    # Swagger UI Documentation
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Add admin dashboard only in dev environment
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]