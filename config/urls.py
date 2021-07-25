from django.contrib import admin
from django.urls import include, path

from rest_framework.authtoken import views as auth_views
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path("", include("apps.users.urls", namespace='users')),
]
