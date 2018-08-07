
from django.conf.urls import url, include

from admin import views

urlpatterns = [
    url('^login/', views.login, name='login'),
    url('^index/', views.index, name='index'),
    url('^register/', views.register, name='register'),
    url('^logout/', views.logout, name='logout'),
    url('^product_list/', views.product_list, name='product_list'),
    url('^product_detail/', views.product_detail, name='product_detail'),
    url('^product_recycle/', views.product_recycle, name='product_recycle'),
    url('^recycle_bin/', views.recycle_bin, name='recycle_bin'),
    url('^product_recover', views.product_recover, name='product_recover'),
    url('^product_remove/', views.product_remove, name='product_remove'),
]
