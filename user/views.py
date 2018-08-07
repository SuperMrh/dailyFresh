import re
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from rest_framework import mixins, viewsets

# Create your views here.
from user.models import UserModel, UserTicketModel
from utils import status_code

# 用户登录视图函数
from user.serializer import UserSerializer
from utils.functions import get_ticket


# 定义用户资源模型
class UserSource(mixins.ListModelMixin,
                 viewsets.GenericViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


# 用户注册视图函数 / 返回用户注册页面
def register(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')

    if request.method == 'POST':
        # 从POST中取到ajax传递过来的参数
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        address = request.POST.get('address')

        # 查找数据库中有没有相同user_name的数据
        user = UserModel.objects.filter(username=user_name)
        if user:
            # 注册用户名已经存在
            return JsonResponse(status_code.USER_REGISTER_NAME_EXIST)
        # 填写参数不完整
        if not all([user_name, pwd, cpwd, email, tel]):
            return JsonResponse(status_code.USER_REGISTER_INFO_INCOMPLETE)
        # 确认密码失败
        if pwd != cpwd:
            return JsonResponse(status_code.USER_REGISTER_PASSWORD_AUTHENTICATION_FAILED)
        # 验证邮箱格式
        if not re.match('^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse(status_code.USER_REGISTER_EMAIL_FORMAT_ERROR)
        # 验证手机号码
        if not re.match('^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$', tel):
            return JsonResponse(status_code.USER_REGISTER_TEL_FORMAT_ERROR)
        # 验证用户名
        if len(user_name) < 5 or len(user_name) > 20:
            return JsonResponse(status_code.USER_REGISTER_NAME_LENGTH_ERROR)
        # 注册用户名不存在，创建数据库记录 --> 密码加密
        password = make_password(pwd)
        UserModel.objects.create(username=user_name,
                                 password=password,
                                 email=email,
                                 tel=tel,
                                 address=address)
        return JsonResponse(status_code.SUCCESS)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')

    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        # 验证信息是否完整
        if not all([user_name, password]):
            return JsonResponse(status_code)
        # 验证用户是否存在
        if not UserModel.objects.filter(username=user_name).exists():
            return JsonResponse(status_code.USER_LOGIN_USERNAME_NOT_EXIST)
        # 验证密码是否正确
        user = UserModel.objects.filter(username=user_name).first()
        name = user.username
        if not check_password(password, user.password):
            return JsonResponse(status_code.USER_LOGIN_PASSWORD_AUTHENTICATION_FAILED)
        # 验证成功，将登陆信息写入浏览器cookies和数据库的user_ticket表
        res = JsonResponse(status_code.SUCCESS)
        # 生成用户ticket
        user_ticket = get_ticket()
        # 指定失效时间
        out_time = datetime.now() + timedelta(days=1)
        # 将ticket写入浏览器
        res.set_cookie('user_ticket', user_ticket, expires=out_time)

        # 创建ticket对象，将ticket写入数据库
        UserTicketModel.objects.create(user_id=user.id, user_ticket=user_ticket, out_time=out_time)
        return res


def logout(request):
    # 取到请求的user
    user = request.user
    # 删除该user的登陆信息
    UserTicketModel.objects.filter(user_id=user.id).delete()
    return HttpResponseRedirect(reverse('demo:index'))
