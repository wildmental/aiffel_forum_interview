from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 스태프이거나 소유자인 경우 모든 동작 가능
        if request.user.is_staff or obj.user == request.user:
            return True
        # 그 외 유저는 조회만 가능
        elif request.method in SAFE_METHODS:
            return True
        else:
            return False
