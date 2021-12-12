# Generated by Django 3.2.9 on 2021-12-08 00:35

import django.core.validators
from django.db import migrations, models
import mainapp.mixin


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0006_alter_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='users_image', validators=[mainapp.mixin.MaxSizeValidator(2), django.core.validators.FileExtensionValidator(['.jpg', '.png'], message='Файл должен иметь расширение .jpg или .png')], verbose_name='Аватар'),
        ),
    ]