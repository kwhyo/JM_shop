# Generated by Django 3.1.2 on 2020-11-01 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_order_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller',
        ),
    ]
