from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    set permission to woners only to edit
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
    

class IsRegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff = True

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff = False
