# Generated by Django 3.1.2 on 2020-11-04 14:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20201104_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='구매날짜'),
        ),
    ]
