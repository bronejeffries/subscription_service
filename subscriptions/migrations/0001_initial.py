# Generated by Django 4.1.5 on 2023-01-11 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('subscriber_ref', models.CharField(max_length=250)),
                ('subscriber_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subscriber_contact', models.CharField(blank=True, max_length=15, null=True)),
                ('susbcriber_extras', models.JSONField(help_text='subscribers details')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default='pending', max_length=25)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.package')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]