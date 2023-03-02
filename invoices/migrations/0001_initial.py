# Generated by Django 4.1.5 on 2023-01-21 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('service', 'Service Payment'), ('subscription', 'Subscription Payment')], max_length=35)),
                ('effective_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('amount', models.FloatField()),
                ('object_id', models.PositiveIntegerField()),
                ('owner_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_object_content', to='contenttypes.contenttype')),
                ('owner_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['content_type', 'object_id'], name='invoices_in_content_b52f81_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['owner_content_type', 'owner_id'], name='invoices_in_owner_c_f94653_idx'),
        ),
    ]