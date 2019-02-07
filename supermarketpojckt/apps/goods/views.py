from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from db.app_common import get_car_key, json_msg
from db.base_view import JudgeSignIn
from goods.models import GoodsClassModel, GoodsSKUModel, PhotoAlbumModel


# 商品首页
class Index(View):
    def get(self, request):
        return render(request, 'goods/index.html')


# 商品分类(商品列表)
class Category(View):
    def get(self, request, classid=0, sortgoods=0):
        # 接收当前分类
        classid = int(classid)
        # 接收排序索引
        sortgoods = int(sortgoods)
        # 自定义排序列表
        sortlist = ['id', '-sales', 'price', '-price', 'add_time']
        # 查询分类表
        goodsclass = GoodsClassModel.objects.filter(is_delete=False)
        total = 0
        # 查询对应的商品
        if classid == 0:
            goods = GoodsSKUModel.objects.filter(goodsclass_id=1).order_by(sortlist[sortgoods])
            # 获取购物车中的总的商品的数量
            user_id = request.session.get("id")
            cnn = get_redis_connection("default")
            car_key = get_car_key(user_id)
            car_values = cnn.hvals(car_key)  # 保存到redis中的数据是 二进制编码了, 需要解码才能使用

            for v in car_values:
                total += int(v)
        else:
            goods = GoodsSKUModel.objects.filter(goodsclass_id=classid).order_by(sortlist[sortgoods])


        context = {
            "goods": goods,  # 对应的商品
            "goodsclass": goodsclass,  # 分类表
            "classid": classid,  # 当前分类
            "sortgoods": sortgoods,  # 当前排序索引
            "total": total,  # 购物车总数量
        }
        return render(request, 'goods/category.html', context=context)


# 商品详情
class Detail(View):
    def get(self, request, goodsid):
        goodsid = int(goodsid)
        sku = GoodsSKUModel.objects.filter(pk=goodsid)
        photo = PhotoAlbumModel.objects.filter(goodsSKU=sku)
        context = {
            "goods": sku,
            "photo": photo,
        }
        return render(request, 'goods/detail.html', context=context)



# 购物车加减数量
class AddReduceCar(View):
    def post(self, request):
        # 1. 判断用户是否登录
        user_id = request.session.get("id")
        if user_id is None:
            return JsonResponse({"error": 1, "msg": "没有登录,请登录!"})

        # 2. 接收请求参数
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # 判断参数合法性
        # 1.都要是整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse({"error": 2, "msg": "参数错误!"})

        # 2.商品必须要存在
        try:
            goods_sku = GoodsSKUModel.objects.get(pk=sku_id)
        except GoodsSKUModel.DoesNotExist:
            return JsonResponse({"error": 3, "msg": "商品不存在!"})

        # 3.库存判断
        if goods_sku.stock < count:
            return JsonResponse({"error": 4, "msg": "库存不足!"})

        # 将购物车数据添加到redis中
        # 链接redis
        cnn = get_redis_connection("default")
        # 操作redis
        # 准备key
        car_key = get_car_key(user_id)

        # 添加
        # 获取购物车中已经存在的数量 加 上 需要添加 与 库存进行比较
        old_count = cnn.hget(car_key, sku_id)  # 二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(5, "库存不足!"))
        rs_count = cnn.hincrby(car_key, sku_id, count)
        if rs_count <= 0:
            # 删除field
            cnn.hdel(car_key, sku_id)

        # 获取购物车中的总的商品的数量
        car_values = cnn.hvals(car_key)  # 保存到redis中的数据是 二进制编码了, 需要解码才能使用
        total = 0
        for v in car_values:
            total += int(v)

        return JsonResponse({"error": 0, "msg": "添加成功", "total": total})
