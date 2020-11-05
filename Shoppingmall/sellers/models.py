from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Seller(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.
    
    sellerID = models.CharField(max_length=64,verbose_name = '아이디')
    password = models.CharField(max_length=64,verbose_name = '비밀번호')
    company_name = models.CharField(max_length=64,verbose_name = '회사명')
    postcode = models.CharField(max_length=64,verbose_name = '우편번호')
    address = models.CharField(max_length=64,verbose_name = '주소')
    phone = models.CharField(max_length=64,verbose_name = '전화번호')
    e_mail = models.CharField(max_length=64,verbose_name = '이메일')
    corporate_number = models.CharField(max_length=64,verbose_name = '사업자등록번호')

    def __str__(self):
        return self.sellerID

class Category(models.Model):
    name = models.CharField(max_length=40, null=False)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 32, verbose_name="상품제목")
    price = models.CharField(verbose_name = "상품가격",default=0,max_length = 32)
    description = RichTextUploadingField(blank=True,null=True,verbose_name="상품설명")
    stock = models.IntegerField(verbose_name="재고",default=1)
    image = models.ImageField(verbose_name="대표사진",null = True,upload_to="")
    upload_date = models.DateTimeField(default=timezone.now,verbose_name="등록날짜")
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE,verbose_name="카테고리")
    view = models.IntegerField(verbose_name = "조회수", null = True, default = 0)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    shipping_fee = models.IntegerField(verbose_name = "배송비", default = 0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['seller']
    
#공지사항 database
class Notice(models.Model):
    author = models.ForeignKey(Seller,on_delete=models.CASCADE)
    title = models.CharField(verbose_name='제목',max_length=200)
    content = models.TextField(verbose_name='내용', default='')
    pub_date = models.DateTimeField(verbose_name='날짜',default= timezone.now)
    # view_count = models.DateTimeField

    # class Meta:
    #     verbose_name= 'notice'
    #     verbose_name_plural='notices'
    #     db_table='blog_notice'
    #     ordering = ('-mod_date')
    class Meta:
        ordering = ['-pub_date']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notice_detail', args=[str(self.id)])

    def get_absolute_url2(self):
        return reverse('usernotice_detail', args=[str(self.id)])