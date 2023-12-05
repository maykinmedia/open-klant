from rest_framework.permissions import BasePermission
from vng_api_common.permissions import bypass_permissions


class TokenPermissions(BasePermission):
    def has_permission(self, request, view):
        if bypass_permissions(request):
            return True

        if not request.auth:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if bypass_permissions(request):
            return True

        if not request.auth:
            return False

        return True
