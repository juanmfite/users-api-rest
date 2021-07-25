from rest_framework import permissions


class UserCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        permission = True
        if view.action == 'create':
            permission = self._has_create_permission(request, view)
        if view.action == 'destroy':
            permission = self._has_destroy_permission(request, view)
        return permission

    def _has_create_permission(self, request, view) -> bool:
        return request.user.staff_or_superuser

    def _has_destroy_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True
        elif request.user.is_staff:
            return request.user.pk == int(view.kwargs['pk'])
        else:
            False
