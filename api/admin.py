from django.contrib import admin

from api.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "company_name", "date_created", "date_updated", )
    fields = ("email", ("first_name", "last_name",), ("phone", "mobile"), "company_name", "sales_contact")
    search_fields = ['email', 'company_name']
    search_help_text = "Client email / Company"


admin.site.register(Client, ClientAdmin)
