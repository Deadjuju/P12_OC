from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as ValidationErrorDRF


def _is_phone_number_valid(phone_number: str) -> bool:
    """ Check if phone number is valid """

    return bool(len(phone_number) >= 10 and phone_number.isdigit())


def _format_phone_number(phone_number: str) -> str:
    """ Format the phone number by removing dots and spaces """

    formatted_phone_number = phone_number.replace(" ", "").replace(".", "")
    return formatted_phone_number


def validate_phone_number(phone_number: str, is_from_serializer: bool = False) -> str:
    """ format and validate phone number """

    phone_number = _format_phone_number(phone_number)
    if not _is_phone_number_valid(phone_number):
        if is_from_serializer:
            raise ValidationErrorDRF(f"ERROR (Phone number): |--> {phone_number} <--| is an invalide format.")
        raise ValidationError(f"ERROR (Phone number): |--> {phone_number} <--| is an invalide format.")
    return phone_number
