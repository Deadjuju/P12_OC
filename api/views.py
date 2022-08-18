import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event
from api.permissions import (IsCommercial,
                             IsCommercialOrSupportReadAndUpdateEvents,
                             IsCommercialOrSupportReadOnlyClients)
from api.serializers import (ClientDetailSerializer,
                             ClientListSerializer,
                             ContractDetailSerializer,
                             ContractListSerializer,
                             EventDetailSerializer,
                             EventListSerializer)


class MultipleSerializerMixin:
    """
    Choice of serializer according to the type of action.
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super(MultipleSerializerMixin, self).get_serializer_class()


# -------------------------------- Client --------------------------------

class ClientViewset(MultipleSerializerMixin,
                    ModelViewSet):
    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadOnlyClients]
    http_method_names = ['get', 'post', 'patch']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['company_name', 'email']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name', 'email']

    def get_serializer_context(self):
        print("CONTEXT")
        context = super(ClientViewset, self).get_serializer_context()
        context.update({"current_user": self.request.user})
        return context

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


# -------------------------------- Contract --------------------------------
# class ContractFilter(django_filters.FilterSet):
#     client = django_filters.CharFilter()
#     client__company_name = django_filters.CharFilter(field_name='client', lookup_expr='company_name')
#     client__email = django_filters.CharFilter(field_name='client', lookup_expr='email')
#
#     amount = django_filters.NumberFilter(field_name='amount', lookup_expr='amount')
#     amount__gt = django_filters.NumberFilter(field_name='amount', lookup_expr='amount__gt')
#     amount__lt = django_filters.NumberFilter(field_name='amount', lookup_expr='amount__lt')
#
#     date = django_filters.DateFilter(field_name='payment_due', lookup_expr='date')
#
#     class Meta:
#         model = Contract
#         fields = ['client', 'amount', 'date']


class ContractViewset(MultipleSerializerMixin,
                      ModelViewSet):
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, IsCommercial]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client__company_name', 'client__email', 'payment_due', 'amount', ]
    # filterset_class = ContractFilter

    def get_serializer_context(self):
        context = super(ContractViewset, self).get_serializer_context()
        context.update({"seller": self.request.user})
        return context

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


# -------------------------------- Event --------------------------------

class EventViewset(MultipleSerializerMixin,
                   ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadAndUpdateEvents]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client__company_name', 'client__email', 'event_date']

    def get_serializer_context(self):
        context = super(EventViewset, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context
