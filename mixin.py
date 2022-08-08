from datetime import datetime

from django.db import models


class DateMixin(models.Model):
    class Meta:
        abstract = True

    date_created: datetime = models.DateTimeField(auto_now_add=True)
    date_updated: datetime = models.DateTimeField(auto_now=True)
