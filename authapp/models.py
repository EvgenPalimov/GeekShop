from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _

# Create your models here.
class MaxSizeValidator(MaxValueValidator):
    message = _('Размер - аватара, не может превышать %(limit_value)s Мб.')

    def __call__(self, value):
        # get the file size as cleaned value
        cleaned = self.clean(value.size)
        params = {'limit_value': self.limit_value, 'show_value': cleaned, 'value': value}
        if self.compare(cleaned, self.limit_value * 1024 * 1024): # convert limit_value from MB to Bytes
            raise ValidationError(self.message, code=self.code, params=params)


class User(AbstractUser):
    image = models.ImageField(verbose_name='Аватар', upload_to='users_image',
                              blank=True, validators=[MaxSizeValidator(2)])
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)

