from django.contrib import admin
from .models import *  # 같은 경로의 models.py에서 User라는 클래스를 임포트한다.
# Register your models here.
# admin DB에 데이터 등록
admin.site.register(Seller)
admin.site.register(Item)
admin.site.register(Category)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date')  # ,'author'
    list_filter = ('pub_date',)
    search_fields =  ('title', 'content')
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)

