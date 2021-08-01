from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # 소유자만 접근 가능
        return obj.user == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # 소유자 외 조회 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        # 소유자만 수정삭제 가능
        return obj.user == request.user
