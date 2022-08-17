from django.contrib.auth.models import AnonymousUser
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
    permission_classes = [IsAuthenticated, IsCommercialOrSupportReadOnlyClients]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        """
        Commercials can read all clients and access only their clients
        Supports can read only their clients
        """

        clients = Client.objects.all()
        user = self.request.user
        if user.role == "SUPPORT":
            events = Event.objects.filter(support_contact=user)
            clients = list(set([event.client for event in events]))
        if self.action == "list":
            return clients
        if user.role == "COMMERCIAL":
            return Client.objects.filter(sales_contact=user)
        return clients

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


# -------------------------------- Contract --------------------------------

class ContractViewset(MultipleSerializerMixin,
                      ModelViewSet):
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated, IsCommercial]
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_context(self):
        context = super(ContractViewset, self).get_serializer_context()
        context.update({"seller": self.request.user})
        return context

    def get_queryset(self):
        all_contracts = Contract.objects.all()
        if self.action == "list":
            contracts = Contract.objects.filter(sales_contact=self.request.user.id)
            return contracts
        return all_contracts

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

    def get_serializer_context(self):
        context = super(EventViewset, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context
