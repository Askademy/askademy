from rest_framework.permissions import BasePermission

class FeedsAuthentication(BasePermission):
    def has_permission(self, request, view):
        return True