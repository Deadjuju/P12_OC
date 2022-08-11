import pprint

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.models import Client, Contract
from api.serializers import (ClientDetailSerializer,
                             ClientListSerializer,
                             ContractDetailSerializer,
                             ContractListSerializer)


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

    # def create(self, request, *args, **kwargs):
    #     print("/" * 150)
    #     pprint.pprint(request.POST)
    #     data = {
    #         "first_name": request.POST.get('first_name'),
    #         "last_name": request.POST.get('last_name'),
    #         "email": request.POST.get('email'),
    #         "company_name": request.POST.get('company_name'),
    #         "phone": request.POST.get('phone'),
    #         "mobile": request.POST.get('mobile'),
    #         "is_confirmed_client": request.POST.get('is_confirmed_client'),
    #     }
    #     print("-- DATA --")
    #     print(data)
    #     serializer = self.serializer_class(data=data)
    #     print("-" * 150)
    #     print(serializer)
    #     if serializer.is_valid():
    #         print("VALID!!!")
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         print("INVALID!!!!!")
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------- Contract --------------------------------

class ContractViewset(MultipleSerializerMixin,
                      ModelViewSet):

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer

    def get_queryset(self):
        return Contract.objects.all()


