import django_filters.rest_framework as drf_filters

from api.models import Client, Contract, Event


# -------------------------------- Client --------------------------------


class ClientFilterSet(drf_filters.FilterSet):
    """Implements filters to be used with ClientViewset."""

    name = drf_filters.CharFilter(
        field_name="company_name", lookup_expr='iexact'
    )
    name_contains = drf_filters.CharFilter(
        field_name="company_name", lookup_expr='icontains'
    )
    email = drf_filters.CharFilter(
        field_name="email", lookup_expr='iexact'
    )
    email_contains = drf_filters.CharFilter(
        field_name="email", lookup_expr='icontains'
    )

    class Meta:
        model = Client
        fields = ['name',
                  'name_contains',
                  'email',
                  'email_contains']


# -------------------------------- Contract --------------------------------

class ContractFilterSet(drf_filters.FilterSet):
    """Implements filters to be used with ContractViewset."""

    client = drf_filters.CharFilter(
        field_name="client", lookup_expr='company_name'
    )
    client_contains = drf_filters.CharFilter(
        field_name="client", lookup_expr='company_name__icontains'
    )
    client_email = drf_filters.CharFilter(
        field_name="client", lookup_expr='email'
    )
    client_email_contains = drf_filters.CharFilter(
        field_name="client", lookup_expr='email__icontains'
    )
    min_amount = drf_filters.NumberFilter(
        field_name="amount", lookup_expr='gte'
    )
    max_amount = drf_filters.NumberFilter(
        field_name="amount", lookup_expr='lte'
    )
    date = drf_filters.DateFilter(field_name='payment_due')

    class Meta:
        model = Contract
        fields = ['client',
                  'client_contains',
                  'client_email',
                  'client_email_contains',
                  'amount',
                  'min_amount',
                  'max_amount',
                  'date']


# -------------------------------- Event --------------------------------

class EventFilterSet(drf_filters.FilterSet):
    """Implements filters to be used with EventViewset."""

    client = drf_filters.CharFilter(
        field_name="client", lookup_expr='company_name'
    )
    client_contains = drf_filters.CharFilter(
        field_name="client", lookup_expr='company_name__icontains'
    )
    client_email = drf_filters.CharFilter(
        field_name="client", lookup_expr='email'
    )
    client_email_contains = drf_filters.CharFilter(
        field_name="client", lookup_expr='email__icontains'
    )
    min_event_date = drf_filters.DateFilter(
        field_name="event_date", lookup_expr='gte'
    )
    max_event_date = drf_filters.DateFilter(
        field_name="event_date", lookup_expr='lte'
    )

    class Meta:
        model = Event
        fields = ['client',
                  'client_contains',
                  'client_email',
                  'client_email_contains',
                  'event_date',
                  'min_event_date',
                  'max_event_date']
