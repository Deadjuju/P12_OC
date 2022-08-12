from django.contrib import admin

from users.forms import UserAdminForm
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "role", "date_created", "date_updated")
    fields = ("email", ("first_name", "last_name",), "password", "phone_number", "role")
    search_fields = ['email', ]
    search_help_text = "User email"

    def get_form(self, request, obj=None, change=False, **kwargs):
        print(f"GET FORM: {type(UserAdminForm)}")
        return UserAdminForm

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
