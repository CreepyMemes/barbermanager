from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.urls.auth_urls')),
    path('user/', include('api.urls.user_urls')),
    path('admin/', include('api.urls.admin_urls')),
]