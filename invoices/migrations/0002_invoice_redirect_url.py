# Generated by Django 4.1.5 on 2023-01-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='redirect_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
