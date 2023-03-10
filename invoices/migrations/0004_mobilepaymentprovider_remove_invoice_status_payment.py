# Generated by Django 4.1.5 on 2023-02-26 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('invoices', '0003_invoice_paid_invoice_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobilePaymentProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(choices=[('airtel', 'AIRTEL'), ('mtn', 'MTN')], max_length=50)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='status',
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('provider_id', models.PositiveIntegerField()),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='invoices.invoice')),
                ('provider_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
