from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCommercialClientOrSupportClientReadOnly(BasePermission):

    def has_permission(self, request, view):
        print(f"METHOD: {request.method}")
        if request.method == "DELETE":
            return False
        return bool(request.user.role == "COMMERCIAL")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user == obj.sales_contact)
