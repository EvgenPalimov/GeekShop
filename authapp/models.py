from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.
from mainapp.mixin import MaxSizeValidator, BaseClassContextMixin


class User(AbstractUser, BaseClassContextMixin):
    image = models.ImageField(verbose_name='Аватар', upload_to='users_image',
        blank=True, validators=[MaxSizeValidator(2)])
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)

