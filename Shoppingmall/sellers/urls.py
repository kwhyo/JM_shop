
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [

    path('', views.home, name='home'),


    path('signup',views.signup,name='sellers_signup'),
    path('login',views.login,name='sellers_login'),
    path('logout',views.logout,name='sellers_logout'),
    #path('register/',views.register,name='register'),

    path('register/',views.itemRegister,name='register'),

    path('register/<str:category>/<str:product>/detail',views.detail,name='detail'),
    path('register/<str:category>/<str:product>/detail/delete',views.delete, name='delete'),
    path('register/<str:category>/<str:product>/detail/edit',views.edit, name='edit'),

    path('category/<str:category>/<str:product>',views.product,name='product'),


    path('notice/', views.NoticeListView.as_view(), name='notice'),
    path('notice/addPost', views.notice_addPost, name='notice_addPost'),
    path('notice/<int:pk>', views.NoticeDetailView.as_view(), name='notice_detail'),


    path('mypage/', views.mypage, name='sellermypage'),

    path('mypage/productlist', views.item, name = 'item'),
    path('mypage/orderList', views.order, name='item'),
    path('mypage/order_detail/<int:order_code>', views.order_detail, name='item'),
    path('mypage/enter_tracking_num', views.enter_tracking_num, name='item'),
    path('mypage/change_order_state', views.change_order_state, name='item'),

    path('ckeditor/', include('ckeditor_uploader.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
