import re
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse

from admin.models import AdminTicketModel


class AdminMiddleware(MiddlewareMixin):

    def process_request(self, request):

        paths = ['/admin/login/', '/admin/register/', '/admin/index/', '/media/']

        for path in paths:
            if re.match(path, request.path) or request.path.startswith('/user/') or request.path.startswith('/demo/'):
                return None

        ticket = request.COOKIES.get('admin_ticket')
        if ticket:
            admin_ticket = AdminTicketModel.objects.filter(admin_ticket=ticket).first()
            if not admin_ticket:
                return HttpResponseRedirect(reverse('admin:login'))
            if datetime.utcnow() > admin_ticket.out_time.replace(tzinfo=None):
                AdminTicketModel.objects.filter(admin=admin_ticket.admin).delete()
                return HttpResponseRedirect(reverse('admin:login'))
            else:
                request.admin = admin_ticket.admin

                # 只能单端登录，不同浏览器之间会存在挤下线情况
                # AdminTicketModel.objects.filter(Q(admin=admin_ticket.admin) &
                #                                ~Q(admin_ticket=ticket)).delete()
                # AdminTicketModel.objects.filter(admin=admin_ticket.admin).exclude(admin_ticket=ticket).delete()
                return None
        else:
            return HttpResponseRedirect(reverse('admin:login'))
