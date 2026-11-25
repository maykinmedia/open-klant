from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from vng_api_common.permissions import bypass_permissions


class TokenPermissions(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if bypass_permissions(request):
            return True

        if not request.auth:
            return False

        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: object
    ) -> bool:
        if bypass_permissions(request):
            return True

        if not request.auth:
            return False

        return True
