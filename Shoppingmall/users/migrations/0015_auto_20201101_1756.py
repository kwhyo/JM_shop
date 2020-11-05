# Generated by Django 3.1.2 on 2020-11-01 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_order_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller',
        ),
        migrations.AddField(
            model_name='order',
            name='seller_id',
            field=models.CharField(default='', max_length=64, verbose_name='상품수'),
        ),
    ]
