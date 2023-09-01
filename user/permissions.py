from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    set permission to woners only to edit
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
    

# class IsRegularUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_staff == True

# class IsSuperAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_staff == False
    
from rest_framework.permissions import BasePermission

class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_staff

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

