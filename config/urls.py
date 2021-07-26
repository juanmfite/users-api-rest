from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', auth_views.obtain_auth_token),
    path("", include("apps.users.urls", namespace='users')),
    path('api/token-jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token-jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
