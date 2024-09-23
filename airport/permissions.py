from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllOrAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated
            or (request.user and request.user.is_staff)
        )


class IsAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_staff
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff

        return True
