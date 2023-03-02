# Generated by Django 4.1.5 on 2023-01-11 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('validity_unit', models.CharField(choices=[('day', 'Days'), ('hour', 'Hours')], default='day', max_length=25)),
                ('validity_span', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=25)),
                ('description', models.TextField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=300)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('rate', models.FloatField(help_text='plan billing rate')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.period')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packages.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]