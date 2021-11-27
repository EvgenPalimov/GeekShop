# Generated by Django 3.2.9 on 2021-11-27 11:56

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='users_image', validators=[authapp.models.MaxSizeValidator(2)]),
        ),
    ]
