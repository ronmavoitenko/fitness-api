from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

# Create your permissions here.


class ReadOnly(BasePermission):
    message = _("You do not have permission to perform this action.")

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsUserOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.activity.id
