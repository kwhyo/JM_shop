# Create your views here.
from django.views import generic
from django.shortcuts import render, redirect
from .models import *
from django.http import Http404
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# crsf_token error
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from users.models import *
from django.db.models import Count, Model
from django.http import HttpResponse, JsonResponse

def home(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    request.session.get('user')
    products = Item.objects.all().order_by('-view')
    # 모든 item을 product_list에 저장
    list['products'] = products
#
#
#     seller_id = request.session.get('seller')
#     print(seller_id)
#     if seller_id:
#         seller_info = Seller.objects.get(pk=seller_id)
# #        return HttpResponse( .userID)
    return render(request, 'sellers/home.html', list)


def signup(request):  # 회원가입 페이지를 보여주기 위한 함수
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    if request.method == "GET":
        return render(request, 'sellers/signup.html', list)

    elif request.method == "POST":
        ID = request.POST.get('ID', None)  # 딕셔너리형태
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        company_name = request.POST.get('companyname', None)  # 딕셔너리형태
        postcode = request.POST.get('postcode', None)
        address = request.POST.get('address1', None) + \
            request.POST.get('address2', None)
        number = request.POST.get('number', None)
        e_mail = request.POST.get('e_mail', None)
        corporate_number = request.POST.get('corporate_number', None)

        res_data = {}
        if not (ID and company_name and password and re_password and address and number and e_mail and postcode and corporate_number):
            messages.add_message(request, messages.INFO,
                                 '모든 값을 입력해야 합니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.
            return render(request, 'sellers/signup.html', list)

        if password != re_password:
            messages.add_message(request, messages.INFO,
                                 '비밀번호가 다릅니다.')  # 첫번째, 초기지원
            # register를 요청받으면 register.html 로 응답.
            return render(request, 'sellers/signup.html', list)
        else:
            seller = Seller(sellerID=ID, password=make_password(password), company_name=company_name,
                            postcode=postcode, address=address, phone=number, e_mail=e_mail, corporate_number=corporate_number)
            seller.save()
            return redirect('/')


def login(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    response_data = {}
    if request.method == "GET":
        return render(request, 'sellers/login.html', list)

    elif request.method == "POST":
        login_username = request.POST.get('ID', None)
        login_password = request.POST.get('password', None)

        if not (login_username and login_password):
            messages.add_message(request, messages.INFO,
                                 '아이디와 비밀번호를 모두 입력해주세요.')  # 첫번째, 초기지원
        else:
            try:
                seller = Seller.objects.get(sellerID=login_username)
                # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
                if check_password(login_password, seller.password):
                    request.session['seller'] = seller.sellerID
                    print(seller.sellerID)
                    # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                    # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                    return redirect('/sellers')
                else:
                    messages.add_message(
                        request, messages.INFO, '비밀번호가 틀렸습니다.')  # 첫번째, 초기지원

            except Seller.DoesNotExist:
                messages.add_message(request, messages.INFO,
                                     '가입하지 않은 아이디입니다.')  # 첫번째, 초기지원

        return render(request, 'users/login.html', list)


def logout(request):
    if request.session.get('seller'):
        del(request.session['seller'])
    return redirect('/sellers')


def mypage(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myseller_id = request.session.get('seller')
    myseller_info = Seller.objects.get(sellerID=myseller_id)
    list['myseller_info'] = myseller_info
    return render(request, 'sellers/mypage.html', list)


def item(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myseller_id = request.session.get('seller')
    seller = Seller.objects.get(sellerID=myseller_id)
    # objects.get은 한개만 가지고옴( 한개 쿼리가 아니면 오류가 뜸!, but objects.filter은 여러개를 가져올 수 있음)
    items = Item.objects.filter(seller=seller)
    list['items'] = items  # context에 모든 후보에 대한 정보를 저장
    # context로 html에 모든 후보에 대한 정보를 전달
    return render(request, 'sellers/item_summary.html', list)

def order(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myseller_id = request.session.get('seller')
    seller = Seller.objects.get(sellerID=myseller_id)
    # objects.get은 한개만 가지고옴( 한개 쿼리가 아니면 오류가 뜸!, but objects.filter은 여러개를 가져올 수 있음)
    items = Purchase.objects.filter(purchase_seller=seller)
    #items = Order.objects.filter(seller = seller).values('order_code').annotate(Count('id')).values()
    list['orders'] = items  # context에 모든 후보에 대한 정보를 저장
    # context로 html에 모든 후보에 대한 정보를 전달

    return render(request, 'sellers/order_list.html', list)


@csrf_exempt
def enter_tracking_num(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    order_code = request.POST.get('order_code')
    tracking_num = request.POST.get('tracking_num')

    orderList = Order.objects.filter(order_code=order_code)

    for order in orderList:
        order.tracking_number = tracking_num
        order.save()

    info = {}
    info['confirm'] = "ok"
    return JsonResponse(info)

@csrf_exempt
def change_order_state(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}

    order_code = request.POST.get('order_code')
    order_state = request.POST.get('order_state')

    orderList = Order.objects.filter(order_code=order_code)

    for order in orderList:
        order.order_state = order_state
        order.save()

    info = {}
    info['confirm'] = "ok"
    return JsonResponse(info)

def order_detail(request,order_code):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myseller_id = request.session.get('seller')
    seller = Seller.objects.get(sellerID=myseller_id)
    # objects.get은 한개만 가지고옴( 한개 쿼리가 아니면 오류가 뜸!, but objects.filter은 여러개를 가져올 수 있음)
    items = Order.objects.filter(order_code = order_code)
    list['orders'] = items  # context에 모든 후보에 대한 정보를 저장

    shipping_info = Order.objects.filter(order_code=order_code).order_by('item_count').first()
    list['shipping_info'] = shipping_info
    # context로 html에 모든 후보에 대한 정보를 전달
    return render(request, 'sellers/order_list_detail.html', list)


@csrf_exempt
def itemRegister(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            print("@@@")
            post = form.save(commit=False)
            post.upload_date = timezone.now()
            post.save()  # 저장하기

            return render(request, 'sellers/success.html',list)

    # 빈 페이지 띄워주는 기능 -> GET
    else:
        form = RegisterForm()
        list['form']= form
        return render(request, 'sellers/register.html',list )


def product(request, category, product):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    thisproduct = Item.objects.get(name=product)
    list["product"] = thisproduct

    return render(request, 'users/product.html', list)


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


def detail(request, category, product):
    try:
        allcategory = Category.objects.all()
        list = {'allcategory': allcategory}
        thisproduct = Item.objects.get(name=product)
        list["product"] = thisproduct
    except Item.DoesNotExist:
        raise Http404('해당 게시물을 찾을 수 없습니다.')

    return render(request, 'sellers/detail.html', list)


def delete(request, category, product):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    try:

        thisproduct = Item.objects.get(name=product)
        list["product"] = thisproduct
        thisproduct.delete()

    except Item.DoesNotExist:
        raise Http404('해당 게시물을 찾을 수 없습니다.')

    return render(request, 'sellers/success.html',list)


def edit(request, category, product):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    item = Item.objects.get(name=product)

    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=item)
        if form.is_valid():
            print("@@@", form.cleaned_data)
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.description = form.cleaned_data['description']
            item.stock = form.cleaned_data['stock']
            item.image = form.cleaned_data['image']
            item.category = form.cleaned_data['category']
            item.save()

            return render(request, 'sellers/success.html',list)

    # 빈 페이지 띄워주는 기능 -> GET
    else:
        form = RegisterForm(instance=item)
        list['form']=form
        list['writing']=True
        list['now']='edit'

        return render(request, 'sellers/edit.html', list)


class NoticeListView(generic.ListView):

    model = Notice
    paginate_by = 10

    def get_context_data(self, **kwargs):
        allcategory = Category.objects.all()
        a = self.request.session.get('seller')
        notice_list = Notice.objects.all()
        return {"sellerid": a, "notice_list": notice_list, 'allcategory': allcategory}


class NoticeDetailView(generic.DetailView):
    model = Notice

    def get_context_data(self, **kwargs):
        allcategory = Category.objects.all()
        notice = super(NoticeDetailView, self).get_context_data(**kwargs)
        notice['allcategory'] = allcategory
        return notice


def notice_addPost(request):
    allcategory = Category.objects.all()
    list = {'allcategory': allcategory}
    myseller_id = request.session.get('seller')
    list["myseller_id"] = myseller_id
    if request.method == "GET":
        return render(request, 'sellers/notice_addPost.html', list)

    elif request.method == "POST":
        author = Seller.objects.get(sellerID=myseller_id)
        title = request.POST.get('TITLE', None)
        content = request.POST.get('CONTENTS', None)

        res_data = {}
        if not (title and content):
            res_data['error'] = "모든 값을 입력해야 합니다."
            # return render(request, 'sellers/notice_addPost.html', res_data) #register를 요청받으면 register.html 로 응답.

        else:
            # author = "ddd",
            addPost = Notice(title=title, content=content, author=author)
            addPost.save()
            return redirect('/sellers/notice/', list)
