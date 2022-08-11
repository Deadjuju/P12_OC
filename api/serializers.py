from rest_framework.serializers import ModelSerializer
from api.models import Client, Contract, Event, EventStatus
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
                  'payment_due',
                  'event']
        extra_kwargs = {
            'status': {'write_only': True},
            'payment_due': {'write_only': True},
            'event': {'write_only': True},
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
                  'payment_due',
                  'event']


# -------------------------------- Event --------------------------------

class EventListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['id',
                  'client',
                  'attendees',
                  'support_contact',
                  'event_status',
                  'event_date',
                  'notes'
                  ]
        extra_kwargs = {
            'attendees': {'write_only': True},
            'event_date': {'write_only': True},
            'notes': {'write_only': True},
        }


class EventStatusSerializer(ModelSerializer):
    class Meta:
        model = EventStatus
        fields = ['id', 'status', ]


class EventDetailSerializer(ModelSerializer):
    client = ClientDetailSerializer()
    event_status = EventStatusSerializer()

    class Meta:
        model = Event
        fields = ['id',
                  'client',
                  'attendees',
                  'support_contact',
                  'event_status',
                  'event_date',
                  'notes'
                  ]
