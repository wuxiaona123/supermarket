from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from db.app_common import get_car_key
from db.base_view import JudgeSignIn


from goods.models import GoodsSKUModel

# 购物车首页
class Index(View):
    def get(self,request):
        # 在redis中查找
        user_id = request.session.get("id")
        cnn = get_redis_connection("default")
        car_key = get_car_key(user_id)
        allcar = cnn.hgetall(car_key)
        # 把查找到的数据放到列表中
        car = []
        for goodsid, count in allcar.items():
            goodcars=GoodsSKUModel.objects.get(pk=goodsid)
            goodcars.count=count
            car.append(goodcars)
        context = {
            "car":car
        }
        return render(request,'shoppingcarts/shopcart.html',context=context)
    def post(self,request):

        return HttpResponse('去结算')