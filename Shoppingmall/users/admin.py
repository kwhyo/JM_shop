from django.contrib import admin
from .models import *  #같은 경로의 models.py에서 User라는 클래스를 임포트한다.

# Register your models here.
#admin DB에 데이터 등록
admin.site.register(User)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'item','item_count','check_YN','total_price')
    list_filter = ('user',)

admin.site.register(Like)

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('id','user','item','item_count','order_date','postcode','address','detail_address','phone','total_price','order_code','receiver_name','order_state','pay_method','receipt_url')
    list_filter = ('user','item')

@admin.register(Purchase)
class Purchase(admin.ModelAdmin):
    list_display = ('user','main_item','order_date','order_code')
    list_filter = ('user','main_item')

@admin.register(Buy)
class Buy(admin.ModelAdmin):
    list_display = ('id','user','item','item_count','price','buy_date','address','phone','price')
    list_filter = ('user','item')




