from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from api.views import SpectacularJSONAPIView, SpectacularSwaggerViewTopBar


urlpatterns = [
    # Backend API endpoints
    path('api/', include('api.urls')),

    # OpenAPI JSON schema
    path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),

    # Swagger UI Documentation
    path("api/", SpectacularSwaggerViewTopBar.as_view(url_name='schema'), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add admin dashboard only in dev environment
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]