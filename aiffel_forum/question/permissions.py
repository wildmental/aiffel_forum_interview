from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # people can see each other that what words they are learning
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of this.
        return obj.user == request.user
