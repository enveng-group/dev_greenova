# Generated by Django 5.1.6 on 2025-02-28 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mechanisms', '0006_environmentalmechanism_overdue_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environmentalmechanism',
            name='overdue_count',
        ),
    ]
