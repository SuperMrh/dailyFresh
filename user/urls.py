
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from user import views

# 实例化SimpleRouter对象
router = SimpleRouter()
# 注册需要管理的资源和处理视图函数
router.register('users', views.UserSource)

urlpatterns = [
    url('^login/', views.login, name='login'),
    url('^register/', views.register, name='register'),
    url('^logout/', views.logout, name='logout'),
]

# 合并urlpatterns
urlpatterns += router.urls
