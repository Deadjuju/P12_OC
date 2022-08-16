from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCommercialOrSupportReadOnlyClients(BasePermission):
    """
    Commercials can read / post / update
    Supports can read
    """

    def has_permission(self, request, view):
        print(f"METHOD: {request.method}")
        if request.method == "DELETE":
            return False
        return bool(request.user.role == "COMMERCIAL")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user == obj.sales_contact)


class IsCommercial(BasePermission):
    """
    Commercials can read / post / update
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return False
        return bool(request.user.role == "COMMERCIAL")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user == obj.sales_contact)


class IsCommercialOrSupportReadAndUpdateEvents(BasePermission):
    """
    Commercials can read / post / update
    Supports can read / update
    """

    def has_permission(self, request, view):
        """ post method only for commercials """

        if request.method == "DELETE":
            return False
        if request.method == "POST":
            return bool(request.user.role == "COMMERCIAL")
        return bool(request.user.role == "COMMERCIAL" or request.user.role == "SUPPORT")

    def has_object_permission(self, request, view, obj):
        is_support = bool(obj.support_contact == request.user and request.user.role == "SUPPORT")
        is_commercial = bool(request.user.role == "COMMERCIAL" and obj.client.sales_contact == request.user)
        if request.method in SAFE_METHODS:
            return True
        return bool(is_support or is_commercial)
