# Generated by Django 3.1.2 on 2020-11-05 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0004_item_shipping_fee'),
        ('users', '0025_auto_20201105_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchase_seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sellers.seller'),
        ),
    ]
