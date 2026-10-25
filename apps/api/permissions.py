from rest_framework import permissions

class IsStaffOrManager(permissions.BasePermission):
    """
    Allows access only to authenticated staff members or managers.
    Rejects ordinary customers with HTTP 403 Forbidden.
    """
    message = "Administrative privilege required. Ordinary customer accounts are denied."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                getattr(request.user, "is_management_authorized", False)
                or request.user.is_staff
                or request.user.is_superuser
            )
        )


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission allowing only the owner of the object or staff to access/modify it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and (request.user.is_staff or getattr(request.user, "is_management_authorized", False)):
            return True
        return hasattr(obj, "user") and obj.user == request.user
