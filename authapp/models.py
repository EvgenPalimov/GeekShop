from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
from django.utils.timezone import now

from mainapp.mixin import MaxSizeValidator, BaseClassContextMixin


class User(AbstractUser, BaseClassContextMixin):
    image = models.ImageField(verbose_name='Аватар', upload_to='users_image',
        blank=True, validators=[MaxSizeValidator(2)])
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    email = models.EmailField(max_length=255, unique=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        return True