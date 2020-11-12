from django.shortcuts import render, redirect
from users.models import *
from sellers.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Count, Model
from django.utils.dateformat import DateFormat




def home(request):
    request.session.get('user')
    products = Item.objects.all().order_by('-view')
    allcategory = Category.objects.all()
    # 모든 item을 product_list에 저장
    list = {'products': products}
    list['allcategory'] = allcategory

    return render(request, 'users/home.html', list)


def signup(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    return render(request, 'users/signup.html', list)


def users_signup(request):  # 회원가입 페이지를 보여주기 위한 함수
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    current_user = request.session.get('user')

    if request.method == "GET":
        return render(request, 'users/users_signup.html', list)

    elif request.method == "POST":
        ID = request.POST.get('ID', None)  # 딕셔너리형태
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        username = request.POST.get('username', None)  # 딕셔너리형태
        postcode = request.POST.get('postcode', None)
        address = request.POST.get('address1', None)
        detail_address = request.POST.get('address2', None)
        cp1 = request.POST.get('cp1', None)
        cp2 = request.POST.get('cp2', None)
        cp3 = request.POST.get('cp3', None)
        number = cp1+cp2+cp3

        email = request.POST.get('email', None)
        email2 = request.POST.get('email2', None)
        e_mail = email + "@" +email2
        if not (ID and username and password and re_password and address and number and e_mail and postcode):
            messages.add_message(request, messages.INFO,
                                 '모든 값을 입력해야 합니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.

            return render(request, 'users/signup.html', list)

        if password != re_password:
            # return HttpResponse('비밀번호가 다릅니다.')
            messages.add_message(request, messages.INFO,
                                 '비밀번호가 다릅니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.
            return render(request, 'users_signup.html', list)

        else:
            user = User(userID=ID, password=make_password(password), username=username, postcode=postcode,
                        address=address, detail_address=detail_address, phone=number, e_mail=e_mail)
            user.save()
            return render(request, 'users/success.html', list)

            # return render(request, 'home.html', res_data) #register를 요청받으면 register.html 로 응답.

# 회원정보변경
def change_user_info(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    list['notice'] = notice

    if request.method == "GET":
        myuser_id = request.session.get('user')
        myuser_info = User.objects.get(userID=myuser_id)
        list['myuser_info'] = myuser_info

        email1, email2 = [str(i) for i in myuser_info.e_mail.split('@') ]
        list['email1'] = email1
        list['email2'] = email2

        cp1 = myuser_info.phone[0:3]
        cp2 = myuser_info.phone[3:7]
        cp3 = myuser_info.phone[7:11]
        list['cp1'] = cp1
        list['cp2'] = cp2
        list['cp3'] = cp3


        return render(request, 'users/change_user_info.html', list)

    elif request.method == "POST":
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        username = request.POST.get('username', None)  # 딕셔너리형태
        postcode = request.POST.get('postcode', None)
        address = request.POST.get('address1', None)
        detail_address = request.POST.get('address2', None)
        cp1 = request.POST.get('cp1', None)
        cp2 = request.POST.get('cp2', None)
        cp3 = request.POST.get('cp3', None)
        number = cp1+cp2+cp3

        email = request.POST.get('email', None)
        email2 = request.POST.get('email2', None)
        e_mail = email + "@" +email2

        print(username,postcode,address,detail_address,number,e_mail )
        if not (username and password and re_password and address and number and e_mail and postcode):
            messages.add_message(request, messages.INFO,
                                 '모든 값을 입력해야 합니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.

            return render(request, 'users/signup.html', list)

        if password != re_password:
            # return HttpResponse('비밀번호가 다릅니다.')
            messages.add_message(request, messages.INFO,
                                 '비밀번호가 다릅니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.
            return render(request, 'users_signup.html', list)

        else:
            myuser_id = request.session.get('user')

            user = User.objects.get(userID=myuser_id)
            user.password = make_password(password)
            user.username = username
            user.address = address
            user.detail_address = detail_address
            user.postcode = postcode
            user.phone = number
            user.e_mail = e_mail

            user.save()
            return render(request, 'users/success.html', list)

@csrf_exempt
def check_id(request):
    try:
        user = User.objects.get(userID=request.GET['id'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
    }
    return JsonResponse(result)


def login(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    if request.method == "GET":
        return render(request, 'users/login.html', list)

    elif request.method == "POST":
        login_username = request.POST.get('ID', None)
        login_password = request.POST.get('password', None)

        if not (login_username and login_password):
            messages.add_message(request, messages.INFO,
                                 '아이디와 비밀번호를 모두 입력하세요.')  # 첫번째, 초기지원
        else:
            try:
                myuser = User.objects.get(userID=login_username)
                # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
                if check_password(login_password, myuser.password):
                    request.session['user'] = myuser.userID
                    # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                    # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                    return redirect('/')
                else:
                    messages.add_message(
                        request, messages.INFO, '비밀번호가 틀렸습니다.')  # 첫번째, 초기지원
            # 아이디가 존재하지 않을 경우
            except User.DoesNotExist:
                messages.add_message(request, messages.INFO,
                                     '가입하지 않은 아이디입니다.')  # 첫번째, 초기지원

        return render(request, 'users/login.html', list)


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('/')


def mypage(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myuser_id = request.session.get('user')
    myuser_info = User.objects.get(userID=myuser_id)
    list['myuser_info'] = myuser_info
    return render(request, 'users/mypage.html', list)


def notice(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    notice_list = Notice.objects.all()
    list['notice_list'] = notice_list
    return render(request, 'users/notice.html', list)


def noticedetail(request, pk):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    notice = Notice.objects.get(id=pk)
    list['notice'] = notice

    return render(request, 'users/notice_detail.html', list)


def category(request, category):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    # category 테이블에서 해당 카테고리에 관한 값을 받아온다
    try:
        cate = Category.objects.get(name=category)

        sort = request.GET.get('sort', '')  # url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다

        #  products = Item.objects.filter(category = category)
        # 모든 item을 product_list에 저장
        # cate.id를 통해 foreign key 조회 가능
        if sort == 'view':
            products = Item.objects.filter(category=cate.id).order_by('-view')
        elif sort == 'low_price':
            products = Item.objects.filter(
                category=cate.id).order_by('price')  # 오름차순
        elif sort == 'high_price':
            products = Item.objects.filter(
                category=cate.id).order_by('-price')  # 내림차순
        else:
            products = Item.objects.filter(
                category=cate.id).order_by('-upload_date')
        list['products'] = products

        return render(request, 'users/category.html', list)

    except Category.DoesNotExist:
        list['products'] = None
        return render(request, 'users/category.html', list)


def product(request, category, product):

    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    thisproduct = Item.objects.get(name=product)
    thisproduct.view = thisproduct.view + 1
    thisproduct.save()
    list['product'] = thisproduct

    # list['product3'] = thisproduct
    list['product2'] = product
    list['category'] = category

    if request.method == "GET":
        cart = request.GET.get('cart')
        if (cart):
            myuser_id = request.session.get('user')

            item_count = request.GET.get('item_count')
            item = thisproduct
            user = User.objects.get(userID=myuser_id)

            if (Cart.objects.filter(item=item).count()==0):
                addcart = Cart(user=user, item=item, item_count=item_count)
                addcart.save()
            info = {}
            info['confirm'] = "ok"
            return JsonResponse(info)
        else:
            return render(request, 'users/product.html', list)

    return render(request, 'users/product.html', list)

#개인 장바구니
def cart(request, userid):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    user = User.objects.get(userID=userid)
    cartitem = Cart.objects.filter(user=user)
    list['cart'] = cartitem

    return render(request, "users/cart.html", list)

@csrf_exempt
def cart_delete(request, userid):
    print('cart_delete')
    checkArr = request.POST.get('ch_box')
    checklist = checkArr.split(',')
    print(len(checklist))
    for i in checklist:
        cartitem = Cart.objects.get(id=int(i))
        cartitem.delete()
        print('delete ok')
    info = {}
    info['confirm'] = "ok"
    return JsonResponse(info)
    # return render(request, "users/cart.html", list)

#개인 주문/배송현황
def order_list(request,userid):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    user = User.objects.get(userID=userid)
    purchase_list = Purchase.objects.filter(user=user).order_by('-order_date')



    list['purchase']=purchase_list
    #!!!!!!!!!!!!!!!!!!!!!!!!!배송완료가아닐때로 고쳐야함. orderstate=!'배송완료'

    return render(request, 'users/order_list.html', list)

#개인 주문/배송현황
def order_list_detail(request,order_code):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    items = Order.objects.filter(order_code=order_code)
    list['orders'] = items

    shipping_info = Order.objects.filter(order_code=order_code).order_by('item_count').first()
    list['shipping_info'] = shipping_info
    return render(request, 'users/order_list_detail.html', list)


#개인 구매목록
def buylist(request,userid):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    user = User.objects.get(userID=userid)
    order = Order.objects.filter(user=user)
    list['buylist'] = order
    # 나중에 구매한꺼번에 한것대로 꼭 묶어서보여주기!!
    # buydatelist=buy.objects.values_list('buy_date')
    # buydatelist[0].strftime('%Y-%m-%d %H')
    # print(buydatelist)
    # set(buydatelist)
    # print(buydatelist)

    return render(request, 'users/buylist.html', list)

@csrf_exempt
def buylist_delete(request, userid):
    print('buylist_delete')
    checkArr = request.POST.get('ch_box')
    print(checkArr)
    checklist = checkArr.split(',')
    print(len(checklist))
    for i in checklist:
        buyitem = Buy.objects.get(id=int(i))
        buyitem.delete()
        print('delete ok')
    info = {}
    info['confirm'] = "ok"
    return JsonResponse(info)



# 장바구니에서 -->구매 : 사용자의 카트목록 중 선택된 것만 불러오기
@csrf_exempt
def order_form(request, userid):
    print('order form')
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    user = User.objects.get(userID=userid)
    list['user'] = user
    if request.method == "GET":
        print('get')
        checkArr = request.GET.get('ch_box')

        if (checkArr):#check된게있으면
            cartList = Cart.objects.filter(user=user)

            if ( ',' in checkArr): #다중선택이라면
                checklist = checkArr.split(',')
                checkTotal=0
                for Cartitem in cartList:
                    SaveCartitem = Cart.objects.get(id=int(Cartitem.id))
                    print(checklist)
                    if str(Cartitem.id) in checklist:
                        SaveCartitem.check_YN = "Y"
                        SaveCartitem.total_price = int(SaveCartitem.item_count) * int(SaveCartitem.item.price)
                        checkTotal += int(SaveCartitem.item_count) * int(SaveCartitem.item.price)
                    else:
                        SaveCartitem.check_YN = "N"
                    SaveCartitem.save()

            else: #단일 선택이 됬다면
                for Cartitem in cartList:
                    SaveCartitem = Cart.objects.get(id=int(Cartitem.id))
                    checkTotal = 0;
                    if Cartitem.id == int(checkArr):
                        SaveCartitem.check_YN = "Y"
                        SaveCartitem.total_price = int(SaveCartitem.item_count)*int(SaveCartitem.item.price)
                        checkTotal = int(SaveCartitem.item_count) * int(SaveCartitem.item.price)
                    else:
                        SaveCartitem.check_YN = "N"
                    SaveCartitem.save()


                #total = int(cartitem.item_count)*int(cartitem.item.price)
                #buy = Buy(user=user, item=cartitem.item, item_count=cartitem.item_count, postcode=user.postcode,
                #          address=user.address, detail_address=user.detail_address, phone=user.phone, price=total)
                #buy.save()
                checklen=1
                #cartitem.delete()
            info={}
            info['confirm'] = "ok"
            request.session['checkTotal'] = checkTotal
            return JsonResponse(info)

        else:#None이면
            print('else문 None일때')

            checkTotal=request.session.get('checkTotal')

            buy = Buy.objects.filter(user=user)
            cartItems = Cart.objects.filter(check_YN = "Y", user=user)
            # buy = Buy(user=user, item=cartitem.item, item_count=cartitem.item_count, postcode=user.postcode,
            #          address=user.address, detail_address=user.detail_address, phone=user.phone, price=total)

            buylist = cartItems
            list['buylist']=buylist
            list['checkTotal'] = checkTotal
            print(checkTotal)

            return render(request, 'users/order_form.html', list)


    elif request.method=="POST":
        print('post')
        checkArr = request.POST.get('ch_box')
        print(checkArr)


        # #사실버튼누르면으로 바꿔야함..
        # buy = Buy(user=user, item=cartitem.item, item_count=cartitem.item_count, postcode=user.postcode,
        #           address=user.address, detail_address=user.detail_address, phone=user.phone, price=total)
        # buy.save()

    # product = Item.objects.get(name=product)
    # total = product.price * int(quantity)
    #
    # list['product'] = product
    #
    # list['quantity'] = quantity
    #
    # buy = Buy(user=user, item=product, item_count=quantity, postcode=user.postcode,
    #           address=user.address, detail_address=user.detail_address, phone=user.phone, price=total)
    # buy.save()

        return render(request, 'users/order_form.html', list)

# 상세상품페이지 --> 구매하기 : 해당상품만 구매
def only_order_form(request, category, product, quantity):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    myuser_id = request.session.get('user')
    user = User.objects.get(userID=myuser_id)
    list['user'] = user

    product = Item.objects.get(name=product)

    total = int(product.price) * int(quantity)


    list['product'] = product
    list['quantity'] = quantity
    list['total'] = total

    return render(request, 'users/only_order_form.html', list)

@csrf_exempt
def purchase_only_order(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}


    #주문번호 제작
    today = DateFormat(datetime.now()).format('YmdHis')
    print(today);

    myuser_id = request.session.get('user')
    username = request.POST.get('username')
    postcode = request.POST.get('postcode')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')
    detail_address = request.POST.get('detail_address')
    email = request.POST.get('email')
    total =  request.POST.get('total')
    shipping_message = request.POST.get('shipping_message')
    pay_method = request.POST.get('pay_method')
    receipt_url = request.POST.get('receipt_url')

    quantity = request.POST.get('quantity')
    product_id = request.POST.get('product_id')
    item = Item.objects.get(id=product_id)

    print(username, postcode,phone_number,address,email, total,pay_method,receipt_url)
    user = User.objects.get(userID=myuser_id)



    order = Order(user=user, item=item, item_count=quantity, receiver_name=username,seller=item.seller,
                  postcode=postcode,address=address, detail_address=detail_address, phone=phone_number,
                  total_price=total,order_code=int(today),shipping_message=shipping_message, pay_method=pay_method, receipt_url=receipt_url)
    order.save()


    purchase = Purchase(user=user, main_item=item,main_order=order, purchase_count=1, purchase_price=total,order_code=order.order_code,purchase_seller=item.seller)
    purchase.save()

    info = {}
    info['confirm'] = "ok"
    info['order_code'] = int(today)
    return JsonResponse(info)


# 실제결제하기
@csrf_exempt
def purchase(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}


    #주문번호 제작
    today = DateFormat(datetime.now()).format('YmdHis')
    print(today);

    myuser_id = request.session.get('user')
    username = request.POST.get('username')
    postcode = request.POST.get('postcode')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')
    detail_address = request.POST.get('detail_address')
    email = request.POST.get('email')
    total =  request.POST.get('total')
    shipping_message = request.POST.get('shipping_message')
    pay_method = request.POST.get('pay_method')
    receipt_url = request.POST.get('receipt_url')


    print(username, postcode,phone_number,address,email, total,pay_method,receipt_url)
    user = User.objects.get(userID=myuser_id)

    cartList = Cart.objects.filter(user=user)

    purchase_count = 0
    for Cartitem in cartList:
        #SaveCartitem = Cart.objects.get(id=int(Cartitem.id))
        if Cartitem.check_YN == "Y" :
            purchase_count+=1
            main_item = Cartitem
            order = Order(user=user, item=Cartitem.item, item_count=Cartitem.item_count, receiver_name=username,postcode=postcode,seller=Cartitem.item.seller,
                        address=address, detail_address=detail_address, phone=phone_number, total_price=total, order_code = int(today),
                          shipping_message=shipping_message,pay_method=pay_method,receipt_url=receipt_url)
            order.save()
            main_order = order
            Cartitem.delete()

    purchase = Purchase(user=user, main_item=main_item.item,main_order=main_order,
                        purchase_count=purchase_count, purchase_price=total,order_code=main_order.order_code,purchase_seller=Cartitem.item.seller)
    purchase.save()

    info = {}
    info['confirm'] = "ok"
    info['order_code'] = int(today)
    return JsonResponse(info)


def purchase_list(request,order_code):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    myuser_id = request.session.get('user')
    user = User.objects.get(userID=myuser_id)


    orderList = Order.objects.filter(order_code=order_code)
    main_order = Order.objects.filter(order_code=order_code).order_by('item_count').first()
    item_total_price = 0
    for order in orderList:
        item_total_price += int(order.item.price) * int(order.item_count)

    list['user'] = user
    list['orderList'] = orderList
    list['item_total_price'] = item_total_price
    list['main_order'] = main_order
    return render(request, 'users/purchase_list.html', list)


