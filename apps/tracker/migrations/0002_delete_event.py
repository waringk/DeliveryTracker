# Generated by Django 4.1.2 on 2022-10-14 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
    ]