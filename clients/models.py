import logging

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission,
)
from django.core.exceptions import ValidationError
from clients.validators import validate_email, validate_password, validate_username

logger = logging.getLogger()

class ClientManager(BaseUserManager):
    def create_superuser(
        self, 
        username:str, 
        email:str,
        password:str,
    ) -> "Client":
        """Create super user"""
        
        is_username_valid, username_error = validate_username(username)
        is_email_valid, email_error = validate_email(email)
        is_password_valid, password_error = validate_password(password)

        if not (is_username_valid and is_email_valid and is_password_valid):
            if not is_username_valid:
                logger.error(f"ERROR: {username_error}")
            if not is_email_valid:
                logger.error(f"ERROR: {email_error}")
            if not is_password_valid:
                logger.error(f"ERROR: {password_error}")
            raise ValidationError("Validation error")

        client: Client = Client()
        client.email=self.normalize_email(email),
        client.username=username
        client.set_password(raw_password=password)
        client.is_active=True
        client.is_staff=True
        client.is_superuser=True
        client.save()
        return client
    
class Client(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        to=Group, 
        verbose_name="группы",
        related_name="client_groups", 
        blank=True
        )
    user_permissions = models.ManyToManyField(
        to=Permission, 
        verbose_name="разрешения",
        related_name="client_permissions", 
        blank=True
        )

    username = models.CharField(
        verbose_name="никнейм",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
    )
    email = models.EmailField(
        verbose_name="эл. почта",
        max_length=100,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name="активный",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="сотрудник",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="администратор",
        default=False,
    )
    gender = models.CharField(
        verbose_name="пол",
        max_length=10,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"
    objects = ClientManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return f"{self.username} | {self.email} | {self.date_created}"
