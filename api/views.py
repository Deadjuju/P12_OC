from rest_framework.viewsets import ModelViewSet

from api.models import Client, Contract, Event
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

    def get_queryset(self):
        return Client.objects.all()


# -------------------------------- Contract --------------------------------

class ContractViewset(MultipleSerializerMixin,
                      ModelViewSet):
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        return Contract.objects.all()


# -------------------------------- Event --------------------------------

class EventViewset(MultipleSerializerMixin,
                   ModelViewSet):
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer

    def get_queryset(self):
        return Event.objects.all()
