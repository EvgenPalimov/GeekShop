# Generated by Django 3.2.9 on 2021-12-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0013_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, default='RU', max_length=10, verbose_name='язык'),
        ),
    ]
