from rest_framework import permissions

class AuthorOrSuperUserOrAdminOrReadOnly(permissions.BasePermission):
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
        return(
            request.user == obj.author
            or request.user.is_staff
            or request.user.is_superuser
            # как указать модератора is_moderator?
        )