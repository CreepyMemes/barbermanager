from django.contrib import admin
from django.urls import path, include, re_path
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/register/', include('dj_rest_auth.registration.urls')),
    re_path(
        r"^api/auth/register/confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    )
]
