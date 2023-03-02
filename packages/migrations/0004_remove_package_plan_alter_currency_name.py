# Generated by Django 4.1.5 on 2023-01-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_package_billing_model_package_billing_unit_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='plan',
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
