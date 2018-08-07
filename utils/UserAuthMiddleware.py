import re
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse

from user.models import UserTicketModel


# 定义用户中间件类
class UserMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 无阻塞url --> 注意media
        paths = ['/user/login/', '/user/register/', '/demo/index/', '/media/']

        # 对于无阻塞url不做处理
        for path in paths:
            if re.match(path, request.path) or request.path.startswith('/admin/'):
                return None

        # 如果url不属于无阻塞url 做以下处理
        # 取到COOKIES里面的user_ticket
        ticket = request.COOKIES.get('user_ticket')
        # 如果ticket存在，说明用户登陆过
        if ticket:
            # 通过ticket的值去取到user_ticket对象
            user_ticket = UserTicketModel.objects.filter(user_ticket=ticket).first()
            # 如果数据库中没有相关记录，回到登陆页面
            if not user_ticket:
                return HttpResponseRedirect(reverse('user:login'))
            # 判断当前时间是否超过user_ticket的超时时间
            if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                # 超过超时时间，删除所有的数据库中的无效数据，并返回登陆页面重新登陆
                UserTicketModel.objects.filter(user=user_ticket.user).delete()
                return HttpResponseRedirect(reverse('user:login'))
            else:
                # 定义request.user
                request.user = user_ticket.user
                # 删除多余的认证信息，
                # 从UserTicket中查询当前user，并且ticket不等于cookie中的ticket
                # UserTicketModel.objects.filter(Q(user=user_ticket.user) &
                #                                ~Q(user_ticket=ticket)).delete()
                return None
        else:
            return HttpResponseRedirect(reverse('user:login'))
