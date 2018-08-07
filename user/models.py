from django.db import models

# Create your models here.


class UserModel(models.Model):

    # 用户信息

    # 用户名，最大长度20
    username = models.CharField(max_length=20, verbose_name='用户名')
    # 密码，最大长度20，登陆的时候需要做加密处理
    password = models.CharField(max_length=256, verbose_name='密码')
    # 电话
    tel = models.CharField(max_length=20, verbose_name='电话号码')
    # 邮箱
    email = models.CharField(max_length=40, null=True, verbose_name='邮箱')
    # 地址 允许为空
    address = models.CharField(max_length=100, null=True, verbose_name='地址')
    # 是否删除，软删除用，默认False
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta():
        # 定义数据表在数据库中的名字
        db_table = 'tb_user'


class RecipientsModel(models.Model):

    # 收件人地址信息

    # 收件人姓名
    recipients_name = models.CharField(max_length=20, verbose_name='收件人姓名')
    # 收件人地址
    recipients_address = models.CharField(max_length=100, verbose_name='收件人地址')
    # 收件人电话
    recipients_tel = models.CharField(max_length=40, verbose_name='收件人电话')
    # 邮编号码
    recipients_postcode = models.CharField(max_length=20, null=True, verbose_name='邮编号码')
    # 是否删除 软删除
    isDelete = models.BooleanField(default=False, verbose_name='是否删除')
    # 关联外键
    userNum = models.ForeignKey(UserModel)

    class Meta():
        db_table = "tb_recipient"


class UserTicketModel(models.Model):

    # 用户Ticket信息

    # 关联用户
    user = models.ForeignKey(UserModel)
    # 用户ticket字段
    user_ticket = models.CharField(max_length=256)
    # 过期时间
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'tb_ticket'
