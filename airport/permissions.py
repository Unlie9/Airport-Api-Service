from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllOrAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)


class IsAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Проверка разрешений на создание
        if request.method in ['POST']:
            return False  # Запрещаем создание билетов для всех

        # Проверка разрешений на просмотр
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_staff  # Только для администраторов

        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit flights and
    allow all users to view flights.
    """

    def has_permission(self, request, view):
        # Проверка разрешений на создание и изменение
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff

        # Для запросов на чтение (GET, HEAD, OPTIONS) доступ разрешен всем
        return True