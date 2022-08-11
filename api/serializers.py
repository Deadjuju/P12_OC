from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from api.models import Client, Contract
from utils import validate_phone_number


# -------------------------------- Client --------------------------------

class ClientListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id',
                  'company_name',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'mobile',
                  'is_confirmed_client',
                  'sales_contact']
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True},
            'phone': {'write_only': True},
            'mobile': {'write_only': True},
            'is_confirmed_client': {'write_only': True},
            'sales_contact': {'write_only': True},
        }

    @classmethod
    def validate_mobile(cls, value):
        return validate_phone_number(value, is_from_serializer=True)

    @classmethod
    def validate_phone(cls, value):
        return validate_phone_number(value, is_from_serializer=True)

    # def create(self, validated_data):
    #     print("HELLO from - Client List Serializer | save method-")
    #     print("_" * 30)
    #     print(validated_data)
    #     project = Client.objects.create(**validated_data)
    #     print("PROJECT")
    #     project.save()
    #     print("SAVE")
    #     return project


class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id',
                  'first_name',
                  'last_name',
                  'phone',
                  'mobile',
                  'company_name',
                  'is_confirmed_client',
                  'sales_contact']


# -------------------------------- Contract --------------------------------

class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id',
                  'contract_title',
                  'sales_contact',
                  'client',
                  'status',
                  'amount',
                  'payment_due', ]
        extra_kwargs = {
            'status': {'write_only': True},
            'payment_due': {'write_only': True},
        }


class ContractDetailSerializer(ModelSerializer):
    client = ClientDetailSerializer()

    class Meta:
        model = Contract
        fields = ['id',
                  'contract_title',
                  'sales_contact',
                  'client',
                  'status',
                  'amount',
                  'payment_due', ]
