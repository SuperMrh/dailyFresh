from django.db import models

# Create your models here.
from django.db.models import PROTECT


class AdminModel(models.Model):

    # 管理员信息

    # 管理员用户名，最大长度20
    admin_name = models.CharField(max_length=20, verbose_name='管理员用户名')
    # 密码，最大长度20，登陆的时候需要做加密处理
    password = models.CharField(max_length=256, verbose_name='密码')
    # 是否删除，软删除用，默认False
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta():
        # 定义数据表在数据库中的名字
        db_table = 'tb_admin_user'


class AdminTicketModel(models.Model):

    # 用户Ticket信息

    # 关联用户
    admin = models.ForeignKey(AdminModel)
    # 用户ticket字段
    admin_ticket = models.CharField(max_length=256)
    # 过期时间
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'tb_admin_ticket'


class GoodsClassifyModel(models.Model):

    # 商品分类信息
    goods_classify = models.CharField(max_length=20, verbose_name='商品分类')

    class Meta:
        db_table = 'tb_goods_classsify'


class GoodsModel(models.Model):

    # 商品信息
    goods_name = models.CharField(max_length=20, verbose_name='商品名称')
    goods_pic = models.ImageField(upload_to='upload', verbose_name='商品图片')
    goods_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='商品价格')
    goods_specification = models.CharField(max_length=20, default='500g', verbose_name='商品规格')
    goods_ID = models.CharField(max_length=20, verbose_name='商品编号')
    goods_classify = models.ForeignKey(GoodsClassifyModel, verbose_name='商品分类', on_delete=PROTECT)
    goods_label = models.IntegerField(default=1, verbose_name='商品标签')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_goods'
