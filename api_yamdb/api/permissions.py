from rest_framework import permissions


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает анонимному пользователю читать отзывы и комментарии,
    аутентифицированному - читать, публиковать отзывы и комментарии,
    удалять и редактировать свои отзывы и комментарии,
    администратору, модератору и суперпользователю - 
    удалять и редактировать любые отзывы и комментарии.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.is_moderator
                or request.user.is_admin))


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_admin))


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.is_admin))
