from rest_framework import permissions


class IsPostOrAdmin(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)
