from django.contrib import admin

from api.models import Client, Contract


class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "company_name", "date_created", "date_updated", )
    fields = ("email",
              ("first_name", "last_name",),
              ("phone", "mobile"),
              "company_name",
              "is_confirmed_client",
              "sales_contact")
    search_fields = ['email', 'company_name']
    search_help_text = "Client email / Company"


class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_title", "sales_contact", "status")
    fields = ("sales_contact", "client", "status", "amount", "payment_due")
    search_fields = ['client', 'contract_title']
    search_help_text = "Client / contract_title"


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
