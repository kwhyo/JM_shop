from django.db import models
from sellers.models import *
from django.utils import timezone

# Create your models here.

class User(models.Model): #장고에서 제공하는 models.Model를 상속받아야한다.

    userID = models.CharField(max_length=64,verbose_name = '아이디')
    password = models.CharField(max_length=64,verbose_name = '비밀번호')
    username = models.CharField(max_length=64,verbose_name = '사용자명')
    postcode = models.CharField(max_length=64,verbose_name = '우편번호')
    address = models.CharField(max_length=64,verbose_name = '주소')
    detail_address = models.CharField(max_length=64,verbose_name = '상세주소')
    phone = models.CharField(max_length=64,verbose_name = '전화번호')
    e_mail = models.CharField(max_length=64,verbose_name = '이메일')
    
    #admin에서 테이블 이름 설정 
    def __str__(self):
        return self.userID

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_count = models.CharField(max_length=64, verbose_name="상품수")
    check_YN = models.CharField(max_length=2, verbose_name="선택여부", default="N") #선택된 제품 : Y, 선택되지 않은 제품 : N
    total_price = models.IntegerField(verbose_name = "총 가격", default=0)
    #
    # # admin에서 테이블 이름 설정
    # def __str__(self):
    #     return (self.user, self.item)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.user, self.item


class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_count = models.CharField( max_length=64,verbose_name="상품수")
    buy_date=models.DateTimeField(default=timezone.now,verbose_name="구매날짜")
    postcode=models.CharField(max_length=64,verbose_name = '우편번호')
    address = models.CharField(max_length=64,verbose_name = '주소')
    detail_address = models.CharField(max_length=64, verbose_name='상세주소')
    phone = models.CharField(max_length=64, verbose_name='전화번호')
    price = models.IntegerField(verbose_name = "주문가격")
    orderstate=models.CharField(max_length=64,default="주문완료")
    # delibary

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller,null=True, on_delete=models.CASCADE)
    item_count = models.CharField( max_length=64,verbose_name="상품수")
    receiver_name = models.CharField(default="",max_length=64, verbose_name='받는 이')
    order_date=models.DateTimeField(default=timezone.now,verbose_name="구매날짜")
    postcode=models.CharField(max_length=64,verbose_name = '우편번호')
    address = models.CharField(max_length=64,verbose_name = '주소')
    detail_address = models.CharField(max_length=64, verbose_name='상세주소')
    phone = models.CharField(max_length=64, verbose_name='전화번호')
    total_price = models.IntegerField(verbose_name = "결제가격", default=0)
    order_state=models.CharField(max_length=64,default="주문완료",verbose_name = "주문상태")
    order_code = models.IntegerField(verbose_name = "주문번호", default=0)
    shipping_message = models.CharField(default="",max_length=64, verbose_name='배송메세지')
    tracking_number = models.CharField(default="",max_length=64, verbose_name='운송장번호')
    pay_method=models.CharField(max_length=64,default="",verbose_name = "지불방식")
    receipt_url=models.CharField(max_length=255,default="",verbose_name = "매출전표 url")

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    main_order = models.ForeignKey(Order, null=True,on_delete=models.CASCADE)
    purchase_count = models.IntegerField(default=1,verbose_name="상품 가짓수")
    purchase_price = models.IntegerField(default=1,verbose_name="결제 금액")
    order_date = models.DateTimeField(default=timezone.now,verbose_name="구매날짜")
    order_code = models.IntegerField(verbose_name = "주문번호", default=0)
    purchase_seller = models.ForeignKey(Seller,null=True, on_delete=models.CASCADE)
