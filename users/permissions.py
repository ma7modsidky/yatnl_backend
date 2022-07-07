from rest_framework import permissions


class UpdateUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have the same id because the user is updating his info.
        return obj.id == request.user.id
       
