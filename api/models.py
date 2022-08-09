from django.db import models

from mixin import DateMixin
from users.models import Role, User
from utils import validate_phone_number


class Client(DateMixin):
    """Client model"""

    first_name: str = models.CharField(max_length=25, blank=False)
    last_name: str = models.CharField(max_length=25, blank=False)
    email: str = models.EmailField(unique=True, blank=False)
    phone: str = models.CharField(max_length=20, blank=True)
    mobile: str = models.CharField(max_length=20, blank=True)
    company_name: str = models.CharField(max_length=250, blank=False)
    is_confirmed_client: bool = models.BooleanField(verbose_name="Confirmed client", default=False)
    sales_contact: User = models.ForeignKey(to=User,
                                            limit_choices_to={"role": Role.COMMERCIAL.value},
                                            on_delete=models.CASCADE,
                                            related_name="clients",
                                            null=True,
                                            blank=True)

    is_cleaned: bool = False

    @property
    def full_name(self) -> str:
        return f"{self.last_name.upper()} {self.first_name.title()}"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.company_name})"

    def clean(self) -> None:
        self.is_cleaned = True
        if self.phone:
            self.phone = validate_phone_number(self.phone)
        if self.mobile:
            self.mobile = validate_phone_number(self.mobile)

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', ]
