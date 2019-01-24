# 引入富文本字段
from ckeditor_uploader.fields import RichTextUploadingField
# 引入继承类
from django.db import models
# 引入基础类
from db.base_model import BaseModel
# 引入字段验证器
from django.core.validators import MinLengthValidator


# Create your models here.
# 模型一：
# 商品分类表
# ID
# 分类名
# 分类简介
# （添加时间
# 修改时间
# 是否删除，BaseModel已有）
class GoodsClassModel(BaseModel):
    classname = models.CharField(max_length=50, validators=[MinLengthValidator(2)], verbose_name='分类名')
    classbrief = models.CharField(max_length=50, validators=[MinLengthValidator(2)], verbose_name='分类简介')

    class Meta:
        db_table = 'GoodsClassModel'
        verbose_name = '商品分类表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.classname


# 模型二：
# 商品SPU表
# ID
# 名称
# 详情
class GoodsSPUModel(models.Model):
    SPUname = models.CharField(max_length=50, validators=[MinLengthValidator(2)], verbose_name='spu名称')
    SPUdetails = RichTextUploadingField(verbose_name='spu详情')

    class Meta:
        db_table = 'GoodsSPUModel'
        verbose_name = '商品SPU表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.SPUname


# 模型三：
# 商品单位表
# ID
# 单位名（斤，箱）
# (添加时间
# 修改时间
# 是否删除,BaseModel已经有了)
class UnitModel(BaseModel):
    unitname = models.CharField(max_length=10, verbose_name='单位名')

    class Meta:
        db_table = 'UnitModel'
        verbose_name = '商品单位表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.unitname


# 模型四：
# 商品SKU表
# ID
# 商品名
# 简介
# 价格
# 单位    UnitModel
# 库存
# 销量
# LOGO地址
# 是否上架
# 商品分类ID    GoodsClassModel
# 商品spu_id     GoodsSPUModel
# (添加时间
# 修改时间
# 是否删除,BaseModel   已有)
class GoodsSKUModel(BaseModel):
    # 商品名
    goodsname = models.CharField(max_length=50, validators=[MinLengthValidator(2)], verbose_name='商品名')
    # 简介
    goodsbrief = models.CharField(max_length=100, validators=[MinLengthValidator(2)], verbose_name='商品简介')
    # 价格（最高金额为10万，小数最多4个小数点）
    price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='价格')
    # 库存
    stock = models.PositiveIntegerField(verbose_name='库存')
    # 销量
    sales = models.PositiveIntegerField(verbose_name='销量')
    # LOGO地址
    goodslogo = models.ImageField(upload_to='goodslogo/%y%m/%d', verbose_name='商品logo')
    # 是否上架
    choic = (
        (0, '未上架'),
        (1, '已上架'),
    )
    shelves = models.SmallIntegerField(choices=choic, verbose_name='是否上架')
    # 商品分类ID  外键  GoodsClassModel
    goodsclass_id = models.ForeignKey(to=GoodsClassModel, verbose_name='商品分类ID')
    # 商品spu_id   外键  GoodsSPUModel
    spu_id = models.ForeignKey(to=GoodsSPUModel, verbose_name='商品spu_id')
    # 单位 外键   UnitModel
    unit = models.ForeignKey(to=UnitModel, verbose_name='单位')

    class Meta:
        db_table = 'GoodsSKUModel'
        verbose_name = '商品SKU表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.goodsname


# 模型五：
# 商品相册表
# ID
# 图片地址
# 商品SKUID    GoodsSKUModel
# (添加时间
# 修改时间
# 是否删除,   BaseModel  已有)
class PhotoAlbumModel(BaseModel):
    goodsImg = models.ImageField(upload_to='goods/%y%m/%d', verbose_name='商品相册')
    goodsSKU = models.ForeignKey(to=GoodsSKUModel, verbose_name='商品SKU')

    class Meta:
        db_table = 'PhotoAlbumModel'
        verbose_name = '商品相册表'  # 备注：此模型在后台django中admin管理名字为：
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.goodsImg.name





# 首页轮播商品表
# ID
# 名称
# 商品SKUID
# 图片地址
# 排序（order）
# (添加时间
# 修改时间
# 是否删除,   BaseModel  已经存在)
class BannerModel(BaseModel):
    # 名称
    bannerName = models.CharField(max_length=30)
    # 商品SKUID     外键
    goodsSKU = models.ForeignKey(to=GoodsSKUModel, verbose_name='商品SKU')
    # 图片地址
    goodsImg = models.ImageField(upload_to='banner/%y%m/%d', verbose_name='商品相册')
    # 排序（order）
    bannerOrder = models.SmallIntegerField()


    class Meta:
        db_table = 'BannerModel'
        verbose_name = '首页轮播商品表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.bannerName





#
# 首页活动表
# ID
# 名称
# 图片地址
# url地址
class ActivityModel(BaseModel):
    # 名称
    activityName = models.CharField(max_length=30)
    # 图片地址
    imgUrl = models.ImageField(upload_to='activity/%y%m/%d', verbose_name='活动图片')
    # url地址
    urlUrl = models.CharField(max_length=100)

    class Meta:
        db_table = 'ActivityModel'
        verbose_name = '首页活动表'  # 备注：此模型在后台django中admin管理名字为：班级表
        verbose_name_plural = verbose_name  # 复数名
    def __str__(self):
        return self.activityName


