from rest_framework import permissions

publishers_allowed_methods = ['PUT', 'PATCH', 'DELETE', 'POST']


class IsPublisherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in publishers_allowed_methods:
            return request.user.groups.filter(name='publishers').exists()
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.published_by == request.user
