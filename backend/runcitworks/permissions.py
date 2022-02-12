from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """
    Customer permission to only allow owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class SaleIsOwner(permissions.BasePermission):
    """
    Custom permission for Sale to only allow owners of a Sale object
    to view it.

    Trying to achieve DRY(don't repeat yourself) principle, user will be
    obtained from Monthdata instead.

    Just putting it in here, DRY doesn't mean to work roundabouts so that
    you don't have to repeat yourself, but I'm trying things out here, ok?
    """
    def has_object_permission(self, request, view, obj):
        return obj.monthdata.user == request.user
