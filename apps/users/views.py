from rest_framework import (
    authentication,
    permissions,
    status,
    viewsets,
)
from rest_framework.response import Response

from apps.external_services.subscription_service import SubscriptionService
from apps.users.models import User
from apps.users.serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserDetailMinimalSerializer,
    UserPartialUpdateSerializer,
    UserUpdateSerializer
)
from apps.users.permissions import UserCustomPermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-id')
    permission_classes = (permissions.IsAuthenticated, UserCustomPermission)
    authentication_classes = [
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        elif self.action == 'partial_update':
            return UserPartialUpdateSerializer
        elif self.action == 'retrieve':
            return UserDetailMinimalSerializer
        elif self.action == 'retrieve-full':
            return UserDetailSerializer
        elif self.action == 'delete':
            pass

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if (
            request.user.staff_or_superuser or
            request.user.pk == int(kwargs['pk'])
        ):
            self.action = 'retrieve-full'

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        extra_data = self._get_extra_data(
            id=serializer.data.get('id'),
            groups=request.data.get('groups')
        )
        data = {**serializer.data, **extra_data}

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(auth_user=request.user)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        extra_data = self._get_extra_data(
            id=instance.pk,
            groups=request.data.get('groups')
        )
        data = {**serializer.data, **extra_data}

        return Response(data)

    def _get_extra_data(self, id, groups):
        subscription = self._get_subscription_state(id)
        return {
            'subscription': subscription,
            'groups': groups or [],
            'password': '********'
        }

    def _get_subscription_state(self, id):
        service = SubscriptionService()
        response = service.get_subscription_state(id)
        if response.status_code == status.HTTP_200_OK:
            return response.json().get('subscription')
        return 'Not available'
