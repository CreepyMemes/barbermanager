from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.auth_urls')),
    path('admin/', include('api.urls.admin_urls')),
    path('barber/', include('api.urls.barber_urls')),
    path('client/', include('api.urls.client_urls')),
    path('public/', include('api.urls.public_urls')),
    path('image/', include('api.urls.image_urls')),
]