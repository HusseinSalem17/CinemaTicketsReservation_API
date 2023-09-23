from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,object):
        if request.method in permissions.SAFE_METHODS:
            return True
        # allow only author of object to edit it
        return object.author == request.user