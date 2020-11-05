# Generated by Django 3.1.2 on 2020-11-04 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_purchase_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='order_code',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='order_date',
        ),
        migrations.AddField(
            model_name='purchase',
            name='main_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.order'),
        ),
    ]
