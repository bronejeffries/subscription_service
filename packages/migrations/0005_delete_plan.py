# Generated by Django 4.1.5 on 2023-01-29 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_remove_package_plan_alter_currency_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Plan',
        ),
    ]
