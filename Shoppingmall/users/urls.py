
from django.urls import path
from . import views

# name : views의 해당 함수를 html 파일에서 name으로 호출할 수 있음


urlpatterns = [

    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('users/signup', views.users_signup, name='users_signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('mypage/', views.mypage, name='usermypage'),


    path('category/<str:category>', views.category, name='category'),
    path('category/<str:category>/<str:product>',
         views.product, name='userproduct'),

    path('notice/', views.notice, name='usernotice'),
    path('notice/<int:pk>', views.noticedetail, name='usernotice_detail'),

    #개인장바구니(top상단카테고리이CART)
    path('cart/<str:userid>', views.cart, name='cart'),
    path('cart/<str:userid>/delete', views.cart_delete, name='cart_delete'),
    #개인주문/배송현황(mypage에서)
    path('order_list/<str:userid>', views.order_list, name='ordering'),
    path('order_list/order_detail/<int:order_code>', views.order_list_detail, name='ordering'),
    #개인구매목록
    path('buylist/<str:userid>', views.buylist, name='buylist'),
    path('buylist/<str:userid>/delete', views.buylist_delete, name='buylist_delete'),




    #실제결제하기
    path('purchase/list/', views.purchase, name='purchase'),
    path('purchase/list/only', views.purchase_only_order, name='purchase'),
    path('purchase_list/<int:order_code>', views.purchase_list, name='purchase_list'),

    #구매하기
    path('category/<str:category>/<str:product>/order_form/<str:quantity>',
         views.only_order_form, name='only_order_form'),  # 상품상세에서 바로 구매하기 -->그상품만 결제
    # 장바구니에서 구매하기로넘어가기 (cartlist조회를 해서 선택한것들 구매)
    path('order_form/<str:userid>', views.order_form, name='order_form'),

]
