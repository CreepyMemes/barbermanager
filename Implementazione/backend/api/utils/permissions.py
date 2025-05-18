from rest_framework.permissions import BasePermission
from ..models import Roles 


class IsAdminRole(BasePermission):
    """
    Allows access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == Roles.ADMIN.value
        )


class IsClientRole(BasePermission):
    """
    Allows access only to users with the CLIENT role.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and request.user.role == Roles.CLIENT.value
        )


class IsBarberRole(BasePermission):
    """
    Allows access only to users with the BARBER role.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and request.user.role == Roles.BARBER.value
        )