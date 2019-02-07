# 引入验证，最大值（长度），最小（长度），正则验证
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, \
    RegexValidator
# 引入继承
from django.db import models

# 引入基础类
from db.base_model import BaseModel


class UserModels(BaseModel):
    # 手机号
    phone = models.CharField(max_length=11, verbose_name='手机号',
                             validators=[RegexValidator(regex=r'^1[34578]\d{9}$', message='手机号码格式不正确')], )
    # 昵称
    nickname = models.CharField(max_length=50, validators=[MinLengthValidator(2)], verbose_name='昵称')
    # 密码
    password = models.CharField(max_length=32, validators=[MinLengthValidator(32)], verbose_name='密码')
    # 性别
    choices = (
        (1, '男'),
        (2, '女'),
        (3, '保密'),
    )
    gender = models.SmallIntegerField(choices=choices, verbose_name='性别', default=3)
    # 头像
    head = models.ImageField(upload_to='user/%y%m/%d', default='user/1901/21/favicon.png', verbose_name='头像')
    # 学校
    school = models.CharField(max_length=50, verbose_name='学校')
    # 老家
    hometown = models.CharField(max_length=100, verbose_name='老家')
    # 位置
    address = models.CharField(max_length=100, verbose_name='老家')
    # 生日
    birthday = models.DateField(auto_now_add=True, verbose_name='生日')

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "user"  # 表名
        verbose_name = '用户表'
        verbose_name_plural = verbose_name





class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="UserModels", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话",
                             max_length=11,
                             validators=[
                                 RegexValidator('^1[3-9]\d{9}$', '电话号码格式错误')
                             ])
    hcity = models.CharField(verbose_name="省", max_length=100, blank=True, null=True)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, null=True)
    harea = models.CharField(verbose_name="区", max_length=100)
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}:{}".format(self.username,self.phone)