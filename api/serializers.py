from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
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

    def validate_client(self, value):
        user_clients = [
            client for client in Client.objects.filter(sales_contact=self.context['seller'])
        ]
        if value in user_clients:
            return value
        raise ValidationError('This client is not assigned to you.')

    @classmethod
    def validate_amount(cls, value):
        if value < 0:
            raise ValidationError('The amount must be positive.')
        return value


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

    def to_representation(self, instance):
        """ check if client is assigned to the seller """

        user_clients = [
            client for client in Client.objects.filter(sales_contact=self.context['seller'])
        ]
        if instance.client in user_clients:
            return super(ContractDetailSerializer, self).to_representation(instance)
        raise exceptions.PermissionDenied(detail="This contract does not belong to one of your clients.")


# -------------------------------- Event --------------------------------

class EventStatusSerializer(ModelSerializer):
    class Meta:
        model = EventStatus
        fields = ['id', 'status', ]


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
        read_only_fields = ('support_contact',)
        extra_kwargs = {
            'attendees': {'write_only': True},
            'event_date': {'write_only': True},
            'notes': {'write_only': True},
        }


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
        read_only_fields = ('support_contact',)

    def to_representation(self, instance):
        """ check if client is assigned to the support """

        user = self.context['user']
        if user.role == "SUPPORT" and (
                instance in [event for event in Event.objects.filter(support_contact=user)]
        ):
            return super(EventDetailSerializer, self).to_representation(instance)
        if user.role == "COMMERCIAL" and user == instance.client.sales_contact:
            return super(EventDetailSerializer, self).to_representation(instance)
        raise exceptions.PermissionDenied(detail="This event does not belong to one of your clients.")
