from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import ClientFilterSet, ContractFilterSet, EventFilterSet
from .models import Client, Contract, Event
from .pagination import SetPagination
from .permissions import (IsCommercialOrSupportReadOnlyContracts,
                          IsCommercialOrSupportReadAndUpdateEvents,
                          IsCommercialOrSupportReadOnlyClients)
from .serializers import (ClientDetailSerializer,
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
    """
    This endpoint gives access to detailed client information.
    To access it, you must at least be connected and belong to the SUPPORT or COMMERCIAL group.
    """

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientDetailSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadOnlyClients]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilterSet
    pagination_class = SetPagination

    def get_serializer_context(self):
        """Add current user to context serializer."""

        context = super(ClientViewset, self).get_serializer_context()
        context.update({"current_user": self.request.user})
        return context

    def perform_create(self, serializer):
        """Save current user in 'sales_contact'."""

        serializer.save(sales_contact=self.request.user)


# -------------------------------- Contract --------------------------------

class ContractViewset(MultipleSerializerMixin,
                      ModelViewSet):
    """
    This endpoint gives access to detailed contract information.
    To access it, you must at least be connected and belong to the SUPPORT or COMMERCIAL group.
    """

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadOnlyContracts]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilterSet
    pagination_class = SetPagination

    def get_serializer_context(self):
        """Add current user (concerns the commercial team) to context serializer"""

        context = super(ContractViewset, self).get_serializer_context()
        context.update({"seller": self.request.user})
        return context

    def perform_create(self, serializer):
        """Save current user in 'sales_contact'."""

        serializer.save(sales_contact=self.request.user)


# -------------------------------- Event --------------------------------

class EventViewset(MultipleSerializerMixin,
                   ModelViewSet):
    """
    This endpoint gives access to detailed event information.
    To access it, you must at least be connected and belong to the SUPPORT or COMMERCIAL group.
    """

    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadAndUpdateEvents]
    http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet
    pagination_class = SetPagination

    def get_serializer_context(self):
        """add user to serializer context"""

        context = super(EventViewset, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context
