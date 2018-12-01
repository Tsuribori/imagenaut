from rest_framework.permissions import BasePermission

class PostPermission(BasePermission):

    def has_permission(self, request, view):
        safe_methods = ['GET', 'POST', 'HEAD', 'OPTIONS']
        if request.method in safe_methods:
            return True
        else:
            return False
