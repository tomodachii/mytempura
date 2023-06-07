from django.db import models
from django.contrib.auth.models import AbstractUser

# from .base import ModelBase
# from django.contrib.auth.hashers import make_password

# import uuid
from django.utils.translation import gettext_lazy as _


# def random_password():
#     return make_password(str(uuid.uuid4()))


# class Account(ModelBase):
#     class Meta:
#         db_table = 'backend_account'
#         ordering = ['pk']
#         verbose_name = _('account')
#         verbose_name_plural = _('accounts')

#     email = models.CharField(max_length=128, null=True, blank=True, editable=False, verbose_name=_('email'), unique=True)
#     name = models.CharField(max_length=256, verbose_name=_('name'))
#     password = models.CharField(max_length=256, default=random_password, verbose_name=_('password'))
#     description = models.TextField(default="", null=True, blank=True, verbose_name=_('description'))

#     def __str__(self):
#         return f'{self.email}'

# Create your models here.

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Account(AbstractUser):
    class Meta:
        db_table = "backend_account"
        ordering = ["pk"]
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    email = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("email"),
        unique=True,
    )
    name = models.CharField(max_length=256, verbose_name=_("name"))
    password = models.CharField(max_length=256, verbose_name=_("password"))
    description = models.TextField(
        default="", null=True, blank=True, verbose_name=_("description")
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email
