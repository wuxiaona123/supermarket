
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator


# Create your models here.
from django.db import models


class UserModels(models.Model):
    # 手机号
    phone = models.CharField(max_length=11, validators=[MinLengthValidator(11),
                                                        RegexValidator(regex=r'^1[34578]\d{9}$', message='手机号码格式不正确')],
                             verbose_name='手机号')
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


    gender = models.SmallIntegerField(choices=choices, verbose_name='性别')
    # 学校
    school = models.CharField(max_length=50, verbose_name='学校')
    # 老家
    hometown = models.CharField(max_length=100, verbose_name='老家')
    # 添加时间
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    # 修改时间
    up_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    # 是否删除
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "user"  # 表名
