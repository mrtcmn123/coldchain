# Generated by Django 5.2.1 on 2025-06-06 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_actionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmovement',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
