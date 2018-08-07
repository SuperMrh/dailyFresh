
from django.conf.urls import url, include

from demo import views

urlpatterns = [
    url('^index/', views.index, name='index'),
]
