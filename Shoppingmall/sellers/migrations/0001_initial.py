from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerID', models.CharField(max_length=64, verbose_name='아이디')),
                ('password', models.CharField(max_length=64, verbose_name='비밀번호')),
                ('company_name', models.CharField(max_length=64, verbose_name='회사명')),
                ('postcode', models.CharField(max_length=64, verbose_name='우편번호')),
                ('address', models.CharField(max_length=64, verbose_name='주소')),
                ('phone', models.CharField(max_length=64, verbose_name='전화번호')),
                ('e_mail', models.CharField(max_length=64, verbose_name='이메일')),
                ('corporate_number', models.CharField(max_length=64, verbose_name='사업자등록번호')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', models.TextField(default='', verbose_name='내용')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='날짜')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Seller')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='상품명')),
                ('price', models.IntegerField(default=0, verbose_name='상품가격')),
                ('description', models.TextField(verbose_name='상품설명')),
                ('stock', models.IntegerField(default=1, verbose_name='재고')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='상품사진')),
                ('detail_image', models.ImageField(null=True, upload_to='', verbose_name='상품상세사진')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='등록날짜')),
                ('view', models.IntegerField(default=0, null=True, verbose_name='조회수')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sellers.Category', verbose_name='카테고리')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellers.Seller')),
            ],
            options={
                'ordering': ['seller'],
            },
        ),
    ]
