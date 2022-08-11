from django.contrib import admin

from api.models import Client, Contract, Event, EventStatus


class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "company_name", "date_created", "date_updated", )
    fields = ("email",
              ("first_name", "last_name",),
              ("phone", "mobile"),
              "company_name",
              "is_confirmed_client",
              "sales_contact")
    search_fields = ["email", "company_name"]
    search_help_text = "Client email / Company"


class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_title", "sales_contact", "status", "date_created", "date_updated",)
    fields = ("sales_contact", "client", "status", "amount", "payment_due", "event")
    search_fields = ["client", "contract_title"]
    search_help_text = "Client / Title"


class EventAdmin(admin.ModelAdmin):
    list_display = ("event_name", "client", "support_contact", "date_created", "date_updated", )
    fields = ("client", "support_contact", "attendees", "event_status", "event_date", "notes")
    search_fields = ["client", "event_status"]
    search_help_text = "Client / Status"


class EventStatusAdmin(admin.ModelAdmin):
    list_display = ("status", )
    fields = ("status", )
    search_fields = ["status", ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus, EventStatusAdmin)
