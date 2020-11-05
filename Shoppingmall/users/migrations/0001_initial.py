
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=64, verbose_name='아이디')),
                ('password', models.CharField(max_length=64, verbose_name='비밀번호')),
                ('username', models.CharField(max_length=64, verbose_name='사용자명')),
                ('postcode', models.CharField(max_length=64, verbose_name='우편번호')),
                ('address', models.CharField(max_length=64, verbose_name='주소')),
                ('detail_address', models.CharField(max_length=64, verbose_name='상세주소')),
                ('phone', models.CharField(max_length=64, verbose_name='전화번호')),
                ('e_mail', models.CharField(max_length=64, verbose_name='이메일')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.CharField(max_length=64, verbose_name='상품수')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_count', models.CharField(max_length=64, verbose_name='상품수')),
                ('buy_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='구매날짜')),
                ('postcode', models.CharField(max_length=64, verbose_name='우편번호')),
                ('address', models.CharField(max_length=64, verbose_name='주소')),
                ('detail_address', models.CharField(max_length=64, verbose_name='상세주소')),
                ('phone', models.CharField(max_length=64, verbose_name='전화번호')),
                ('price', models.IntegerField(verbose_name='주문가격')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
    ]
