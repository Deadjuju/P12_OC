from django.db import models

from mixin import DateMixin
from users.models import Role, User
from utils import validate_phone_number


class Client(DateMixin, models.Model):
    """Client model"""

    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=20, blank=True, default="")
    mobile = models.CharField(max_length=20, blank=True, default="")
    company_name = models.CharField(max_length=250, blank=False)
    is_confirmed_client = models.BooleanField(verbose_name="Confirmed client", default=False)
    sales_contact = models.ForeignKey(to=User,
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

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'company_name', ]

    class Meta:
        ordering = ["company_name"]


class EventStatus(models.Model):
    """Event status possibilities"""

    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status.title()

    class Meta:
        verbose_name_plural = "Event status"


class Event(DateMixin, models.Model):
    """Event model"""

    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name="events_client")
    attendees = models.PositiveIntegerField(default=0)
    support_contact = models.ForeignKey(to=User,
                                        limit_choices_to={"role": Role.SUPPORT.value},
                                        on_delete=models.CASCADE,
                                        related_name="events_support",
                                        null=True,
                                        blank=True)
    event_status = models.ForeignKey(to=EventStatus,
                                     on_delete=models.CASCADE,
                                     related_name="events_status")
    event_date = models.DateField()
    notes = models.TextField(help_text="Important notes", blank=True)

    @property
    def event_name(self) -> str:
        number = f"{'0' * (6 - len(str(self.pk)))}{self.pk}"
        formatted_date = self.event_date.strftime('%m%d%Y')
        name = f"EVENT-{number} - {formatted_date} - ({self.event_status})"
        return name

    def __str__(self) -> str:
        return self.event_name

    class Meta:
        ordering = ["client"]


class Contract(DateMixin, models.Model):
    """Contract model"""

    sales_contact = models.ForeignKey(to=User,
                                      limit_choices_to={"role": Role.COMMERCIAL.value},
                                      on_delete=models.CASCADE,
                                      related_name="commercials",
                                      null=True,
                                      blank=True)
    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name="clients")
    status = models.BooleanField(verbose_name="Contract signed", default=False)
    amount = models.FloatField(verbose_name="Amount (€)")
    payment_due = models.DateField(null=True, blank=True)
    event = models.ForeignKey(to=Event,
                              on_delete=models.CASCADE,
                              related_name="events_contract",
                              blank=True,
                              null=True, )

    @property
    def contract_number(self) -> str:
        return f"{'0' * (6 - len(str(self.pk)))}{self.pk}"

    @property
    def contract_title(self) -> str:
        formatted_date = self.date_created.strftime('%m%d%Y')
        base_title = f"{self.contract_number}__EPICEVENTS__{formatted_date}#{self.client.pk}"
        if not self.status:
            return f"{base_title}_(UNSIGNED)"
        if not self.payment_due:
            return f"{base_title}_(SIGNED / UNPAID)"
        return f"{base_title}_(PAID)"

    def __str__(self) -> str:
        return self.contract_title

    class Meta:
        ordering = ["client"]
