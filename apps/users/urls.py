from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('v1/users', UserViewSet, basename='users')

urlpatterns = router.urls
