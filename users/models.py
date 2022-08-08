from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from mixin import DateMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Role(Enum):
    MANAGEMENT = "MANAGEMENT"
    COMMERCIAL = "COMMERCIAL"
    SUPPORT = "SUPPORT"


class User(AbstractUser, DateMixin):
    """User model."""

    ROLE_CHOICES = [
        (Role.MANAGEMENT.value, "Team Management"),
        (Role.COMMERCIAL.value, "Commercial Team"),
        (Role.SUPPORT.value, "Support Team"),
    ]

    username = None
    email: str = models.EmailField(_('email address'), unique=True)
    password: str = models.CharField(_("password"), max_length=128)
    first_name: str = models.CharField(_("first name"), max_length=150, blank=False)
    last_name: str = models.CharField(_("last name"), max_length=150, blank=False)
    role: Role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=False)

    @property
    def full_name(self) -> str:
        return f"{self.last_name.upper()} {self.first_name.title()}"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        match self.role:
            case Role.MANAGEMENT.value:
                group = Group.objects.get(name='management')
                group.user_set.add(self)
            case Role.COMMERCIAL.value:
                group = Group.objects.get(name='commercial')
                group.user_set.add(self)
            case Role.SUPPORT.value:
                group = Group.objects.get(name='support')
                group.user_set.add(self)

    class Meta:
        ordering = ["email"]

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']
