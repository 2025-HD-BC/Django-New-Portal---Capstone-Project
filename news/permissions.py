from rest_framework import permissions

class IsEditor(permissions.BasePermission):
    """
    Allows access only to users with the editor role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "editor"
        )

class IsJournalistOrEditor(permissions.BasePermission):
    """
    Allows access to journalists and editors.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, "role", None) in ["journalist", "editor"]
        )
