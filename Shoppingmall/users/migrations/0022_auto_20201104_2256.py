# Generated by Django 3.1.2 on 2020-11-04 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_auto_20200809_1945'),
        ('users', '0021_auto_20201103_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='receipt_url',
            field=models.CharField(default='', max_length=255, verbose_name='매출전표 url'),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_count', models.IntegerField(default=1, verbose_name='상품 가짓수')),
                ('purchase_price', models.IntegerField(default=1, verbose_name='결제 금액')),
                ('order_code', models.IntegerField(default=0, verbose_name='주문번호')),
                ('main_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
