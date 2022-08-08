from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", )
    fields = ("email", ("first_name", "last_name",), "password", "phone_number", "role")
    search_fields = ['email', ]
    search_help_text = "User email"


admin.site.register(User, UserAdmin)
