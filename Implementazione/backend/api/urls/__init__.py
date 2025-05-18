from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.auth_urls')),
    path('admin/', include('api.urls.admin_urls')),
    path('public/', include('api.urls.public_urls')),
]