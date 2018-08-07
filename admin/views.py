from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
# Create your views here.

from admin.models import AdminModel, AdminTicketModel, GoodsModel, GoodsClassifyModel
from utils.functions import get_ticket


# 注册视图函数
def register(request):
    # GET请求返回页面
    if request.method == 'GET':
        return render(request, 'admin/register.html')
    # POST页面取到数据添加到数据库
    if request.method == 'POST':
        # 通过request.POST获取注册信息
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # 必填字段必须全部填写，才能完成注册
        if not all([admin_name, password]):
            data = {
                'msg': '必填信息必须填写！'
            }
            # 必填字段未全部填写，跳转到登陆页面，提示信息
            return render(request, 'admin/register.html', data)
        else:
            # 信息全部正确时，将密码进行加密处理，然后创建对象
            if password == cpassword:
                password = make_password(password)
                AdminModel.objects.create(admin_name=admin_name,
                                         password=password)
                # 跳转到登陆页面
                return HttpResponseRedirect(reverse('admin:login'))


# 登陆视图函数
def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')
        # 请求的方式为POST的时候，进行用户登录操作
    if request.method == 'POST':
        # 获取输入的admin_name和password
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        # 判断用户名是否存在
        if AdminModel.objects.filter(admin_name=admin_name).exists():
            # 取到admin
            admin = AdminModel.objects.get(admin_name=admin_name)
            # 检查输入的密码和数据库中的密码是否一致
            admin_id = admin.id
            if check_password(password, admin.password):
                res = HttpResponseRedirect(reverse('admin:index'))  # , kwargs={'user_id': user_id}
                # 生成缓存ticket
                admin_ticket = get_ticket()
                # 指定缓存失效时间
                out_time = datetime.now() + timedelta(days=1)
                # 将ticket写入浏览器
                res.set_cookie('admin_ticket', admin_ticket, expires=out_time)

                # 创建AdminTicketModel对象
                AdminTicketModel.objects.create(admin_id=admin_id, admin_ticket=admin_ticket, out_time=out_time)
                # 跳转到index页面
                return res
            else:
                # 密码验证不对，跳转到登陆页面
                return HttpResponseRedirect(reverse('admin:login'))
        else:
            # 用户名不存在，跳转到登陆页面
            return HttpResponseRedirect(reverse('admin:login'))


# 用户注销视图函数
def logout(request):
    if request.method == 'GET':
        # 取到admin
        admin = request.admin
        # 筛选出AdminTicketModel中的对应的数据
        AdminTicketModel.objects.filter(admin_id=admin.id).delete()
        # 返回登陆页面
        return HttpResponseRedirect(reverse('admin:login'))


# 首页视图函数
def index(request):
    if request.method == 'GET':
        return render(request, 'admin/index.html')


# 产品 列表/筛选 视图函数
def product_list(request):
    if request.method == 'GET':
        num = request.GET.get('page', 1)
        product_classify = request.GET.get('classify', '')
        query_word = request.GET.get('query_word', '')
        goods_classify = GoodsClassifyModel.objects.all()
        classify = GoodsClassifyModel.objects.filter(goods_classify=product_classify).first()
        if all([classify, query_word]):
            goods = GoodsModel.objects.filter(Q(goods_name__icontains=query_word) &
                                              Q(goods_classify=classify.id) &
                                              Q(is_delete=0)).all()
        elif not classify and not query_word:
            goods = GoodsModel.objects.filter(is_delete=0).all()
        else:
            if classify:
                goods = GoodsModel.objects.filter(Q(goods_classify=classify.id) &
                                                  Q(is_delete=0)).all()
            if query_word:
                goods = GoodsModel.objects.filter(Q(goods_name__icontains=query_word) &
                                                  Q(is_delete=0)).all()
        goods_list = []
        for good in goods:
            if good.goods_label == 1:
                title1, title2, title3 = ('是', '否', '否')
                label1, label2, label3 = (89, 88, 88)
            elif good.goods_label == 2:
                title1, title2, title3 = ('否', '是', '否')
                label1, label2, label3 = (88, 89, 88)
            elif good.goods_label == 3:
                title1, title2, title3 = ('否', '否', '是')
                label1, label2, label3 = (88, 88, 89)
            goods_list.append({'good': good, 'title1': title1, 'title2': title2, 'title3': title3,
                               'label1': label1, 'label2': label2, 'label3': label3})
        paginator = Paginator(goods_list, 10)
        try:
            page = paginator.page(num)
        except Exception as e:
            num = int(num) - 1
            page = paginator.page(num)
        start_num = 1 + (int(num) - 1) * 10
        stop_num = int(num) * 5 if int(num) < paginator.num_pages else paginator.count
        data = {
            'page': num,
            'classify': product_classify,
            'query_word': query_word,
            'goods_list': page,
            'start_num': start_num,
            'stop_num': stop_num,
            'goods_classify': goods_classify
        }
        return render(request, 'admin/product_list.html', data)


# 产品详情视图函数
def product_detail(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        goods_classify = GoodsClassifyModel.objects.all()
        good = GoodsModel.objects.filter(id=id).first()
        return render(request, 'admin/product_detail.html', {'goods_classify': goods_classify, 'good': good})

    # 请求为POST的时候添加产品数据到数据库
    if request.method == 'POST':
        id = request.GET.get('id')
        good = GoodsModel.objects.filter(id=id)
        goods_name = request.POST.get('goods_name')
        goods_ID = request.POST.get('goods_ID')
        # 查询goods_ID是否重复
        goods = GoodsModel.objects.filter(goods_ID=goods_ID)
        goods_price = request.POST.get('goods_price')
        goods_classify = request.POST.get('goods_classify')
        classify = GoodsClassifyModel.objects.filter(goods_classify=goods_classify).first()
        goods_specification = request.POST.get('goods_specification')
        goods_label = request.POST.get('goods_label')
        goods_pic = request.FILES.get('goods_pic')
        all_classify = GoodsClassifyModel.objects.all()

        # 数据库中不存在id为id的商品，说明前端是新增商品
        if not good:
            # goods_ID在数据库中已经存在，返回detail页面，返回提示信息
            if goods:
                good = GoodsModel()
                good.goods_name = goods_name
                good.goods_price = goods_price
                good.goods_specification = goods_specification
                good.goods_label = goods_label
                return render(request, 'admin/product_detail.html', {'good': good, 'msg': '商品ID已存在,请重新输入!',
                                                                     'goods_classify': all_classify})
            # goods_ID在数据库中不存在，创建商品，返回页面
            GoodsModel.objects.create(goods_name=goods_name,
                                      goods_ID=goods_ID,
                                      goods_price=goods_price,
                                      goods_classify=classify,
                                      goods_specification=goods_specification,
                                      goods_label=goods_label,
                                      goods_pic=goods_pic)

        else:
            # 在更新的时候，不会根据upload_to去添加前一层级目录，需要手动添加
            goods_pic = 'upload/' + goods_pic.name
            good.update(goods_name=goods_name,
                        goods_ID=goods_ID,
                        goods_price=goods_price,
                        goods_classify=classify,
                        goods_specification=goods_specification,
                        goods_label=goods_label,
                        goods_pic=goods_pic)
        return HttpResponseRedirect(reverse('admin:product_list'))


# 把产品放到回收站视图函数
def product_recycle(request):
    num = request.GET.get('page', 1)
    product_id = request.GET.get('id')
    product_classify = request.GET.get('classify', '')
    query_word = request.GET.get('query_word', '')
    product = GoodsModel.objects.filter(id=product_id).first()
    product.is_delete = True
    product.save()
    """
    return HttpResponseRedirect(reverse('admin:product_list', kwargs={'classify': product_classify, 'query_word': query_word}))  
    
    注意：在使用reverse来进行页面跳转的时候，传递进去的参数kwargs是以'/'而不是以'&'来组建的。
    """
    return HttpResponseRedirect('/admin/product_list/?classify=%s&query_word=%s&page=%s' % (product_classify, query_word, num))


# 产品回收站视图函数
def recycle_bin(request):
    if request.method == 'GET':
        num = request.GET.get('page', 1)
        product_classify = request.GET.get('classify', '')
        query_word = request.GET.get('query_word', '')
        goods_classify = GoodsClassifyModel.objects.all()
        classify = GoodsClassifyModel.objects.filter(goods_classify=product_classify).first()
        if all([classify, query_word]):
            goods = GoodsModel.objects.filter(Q(goods_name__icontains=query_word) &
                                              Q(goods_classify=classify.id) &
                                              Q(is_delete=1)).all()
        elif not classify and not query_word:
            goods = GoodsModel.objects.filter(is_delete=1).all()
        else:
            if classify:
                goods = GoodsModel.objects.filter(Q(goods_classify=classify.id) &
                                                  Q(is_delete=1)).all()
            if query_word:
                goods = GoodsModel.objects.filter(Q(goods_name__icontains=query_word) &
                                                  Q(is_delete=1)).all()
        goods_list = []
        for good in goods:
            if good.goods_label == 1:
                title1, title2, title3 = ('是', '否', '否')
                label1, label2, label3 = (89, 88, 88)
            elif good.goods_label == 2:
                title1, title2, title3 = ('否', '是', '否')
                label1, label2, label3 = (88, 89, 88)
            elif good.goods_label == 3:
                title1, title2, title3 = ('否', '否', '是')
                label1, label2, label3 = (88, 88, 89)
            goods_list.append({'good': good, 'title1': title1, 'title2': title2, 'title3': title3,
                               'label1': label1, 'label2': label2, 'label3': label3})
        paginator = Paginator(goods_list, 10)
        try:
            page = paginator.page(num)
        except Exception as e:
            num = int(num) - 1
            page = paginator.page(num)
        start_num = 1 + (int(num) - 1) * 10
        stop_num = int(num) * 5 if int(num) < paginator.num_pages else paginator.count
        data = {
            'page': num,
            'classify': product_classify,
            'query_word': query_word,
            'goods_list': page,
            'start_num': start_num,
            'stop_num': stop_num,
            'goods_classify': goods_classify
        }
        return render(request, 'admin/recycle_bin.html', data)


# 产品恢复视图函数
def product_recover(request):
    num = request.GET.get('page', 1)
    product_id = request.GET.get('id')
    product_classify = request.GET.get('classify', '')
    query_word = request.GET.get('query_word', '')
    product = GoodsModel.objects.filter(id=product_id).first()
    product.is_delete = False
    product.save()
    return HttpResponseRedirect('/admin/recycle_bin/?classify=%s&query_word=%s&page=%s'
                                % (product_classify, query_word, num))


def product_remove(request):
    num = request.GET.get('page', 1)
    product_id = request.GET.get('id')
    product_classify = request.GET.get('classify', '')
    query_word = request.GET.get('query_word', '')
    GoodsModel.objects.filter(id=product_id).first().delete()
    return HttpResponseRedirect('/admin/recycle_bin/?classify=%s&query_word=%s&page=%s'
                                % (product_classify, query_word, num))
