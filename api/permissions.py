from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Client, Event, Contract
from loggers.warning_logger import PermissionLogger
from users.models import Role


class IsCommercialOrSupportReadOnlyClients(BasePermission, PermissionLogger):
    """
    Commercials can read / post / update
    Supports can read
    """

    def has_permission(self, request, view):
        is_support: bool = bool(request.user.role == Role.SUPPORT.value)
        is_commercial: bool = bool(request.user.role == Role.COMMERCIAL.value)

        if request.method == "DELETE":
            self.warning_logger_delete(request, view, Client)
            return False
        if request.method == "POST" and is_support:
            self.warning_logger_support_post(request, "client")
            return False
        return bool(is_commercial or is_support)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user == obj.sales_contact):
            self.warning_logger_update_not_allowed(request, obj)
            return False
        return bool(request.user == obj.sales_contact)


class IsCommercialOrSupportReadOnlyContracts(BasePermission, PermissionLogger):
    """
    Commercials can read / post / update
    """

    def has_permission(self, request, view):
        is_support: bool = bool(request.user.role == Role.SUPPORT.value)
        is_commercial: bool = bool(request.user.role == Role.COMMERCIAL.value)

        if request.method == "DELETE":
            self.warning_logger_delete(request, view, Contract)
            return False
        if request.method == "POST" and is_support:
            self.warning_logger_support_post(request, "contract")
            return False
        return is_commercial or is_support

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user.role == Role.COMMERCIAL.value):
            self.warning_logger_update_not_allowed(request, obj)
            return False
        return bool(request.user == obj.sales_contact)


class IsCommercialOrSupportReadAndUpdateEvents(BasePermission, PermissionLogger):
    """
    Commercials can read / post / update
    Supports can read / update
    """

    def has_permission(self, request, view):
        """ post method only for commercials """

        is_support: bool = bool(request.user.role == Role.SUPPORT.value)
        is_commercial: bool = bool(request.user.role == Role.COMMERCIAL.value)

        if request.method == "DELETE":
            self.warning_logger_delete(request, view, Event)
            return False
        if request.method == "POST" and is_support:
            self.warning_logger_support_post(request, "event")
            return False
        if request.method == "POST" and is_commercial:
            return bool(request.user.role == Role.COMMERCIAL.value)
        return is_commercial or is_support

    def has_object_permission(self, request, view, obj):
        is_support = bool(obj.support_contact == request.user and request.user.role == Role.SUPPORT.value)
        is_commercial = bool(request.user.role == Role.COMMERCIAL.value and obj.client.sales_contact == request.user)
        if request.method in SAFE_METHODS:
            return True
        if not bool(is_support or is_commercial):
            self.warning_logger_update_not_allowed(request, obj)
            return False
        return True
