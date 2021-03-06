import os
from time import sleep
from alipay import AliPay
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# from cart.hepler import get_cart_key, json_msg
# from db.base_view import VerifyLoginView
# from goods.models import GoodsSKU
# from order.models import Transport, Order, OrderGoods
# from user.models import UserAddress, SpUser
from django_redis import get_redis_connection
from datetime import datetime
import random

from db.app_common import json_msg, get_car_key
from db.base_view import JudgeSignIn
from goods.models import GoodsSKUModel
from orders.models import Transport, Order, OrderGoods, Payment
from supermarketpojckt import settings
from users.models import UserAddress, UserModels


class ConfirmOrder(JudgeSignIn):
    """确认订单页面"""

    def get(self, request):
        """
            1. 如果没有收货地址显示添加收货地址
               如果有收货地址, 显示默认收货地址, 如果没有默认显示第一个


            2. 展示商品信息
                a. 获取商品sku_ids
                    如何获取多个参数的值 getlist() get()只能获取一个

                b. 根据商品id获取商品信息 并且 获取购物车redis中的数量


        """
        user_id = request.session.get("id")
        # >>>> 1. 收货地址处理
        address = UserAddress.objects.filter(user_id=user_id).order_by("-isDefault").first()
        # address = None

        # 处理商品信息
        sku_ids = request.GET.getlist("sku_ids")
        # 准备空列表 装商品
        goods_skus = []
        # 准备商品总计
        goods_total_price = 0

        # 准备redis
        r = get_redis_connection()
        # 准备键
        cart_key = get_car_key(user_id)

        # 遍历
        for sku_id in sku_ids:
            # 商品信息
            try:
                goods_sku = GoodsSKUModel.objects.get(pk=sku_id)
            except GoodsSKUModel.DoesNotExist:
                # 商品不存在就回到购物车
                return redirect("shoppingcart:index")

            # 获取对应商品的数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                # 商品数量不存在就回到购物车
                return redirect("shoppingcart:index")

            # 保存到商品对象上
            goods_sku.count = count

            # 装商品
            goods_skus.append(goods_sku)

            # 统计商品总计
            goods_total_price += goods_sku.price * count

        # 获取运输方式
        transports = Transport.objects.filter(is_delete=False).order_by('price')

        # 渲染数据
        context = {
            'address': address,
            'goods_skus': goods_skus,
            'goods_total_price': goods_total_price,
            'transports': transports,
        }

        return render(request, 'orders/tureorder.html', context=context)

    def post(self, request):
        """
            保存订单数据
            1. 订单基本信息表 和 订单商品表
        """
        # 1. 接收参数
        transport_id = request.POST.get('transport')
        sku_ids = request.POST.getlist('sku_ids')
        address_id = request.POST.get('address')

        # 接收用户的id
        user_id = request.session.get("id")
        user = UserModels.objects.get(pk=user_id)

        # 验证数据的合法性
        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(2, "参数错误"))

        # 验证收货地址和运输方式存在
        try:
            address = UserAddress.objects.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在!"))

        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在!"))

        # 2. 操作数据

        # >>>1 . 操作订单基本信息表
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.brief)
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            transport_price=transport.price,
            transport=transport.name,
            username=address.username,
            phone=address.phone,
            address=address_info
        )

        # >>>2. 操作订单商品表
        # 操作redis
        r = get_redis_connection()
        cart_key = get_car_key(user_id)

        # 准备个变量保存商品总金额
        goods_total_price = 0
        for sku_id in sku_ids:

            # 获取商品对象
            try:
                goods_sku = GoodsSKUModel.objects.get(pk=sku_id, is_delete=False)
            except GoodsSKUModel.DoesNotExist:
                return JsonResponse(json_msg(5, "商品不存在"))

            # 获取购物车中商品的数量
            # redis 基于内存的存储,有可能数据会丢失
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                return JsonResponse(json_msg(6, "购物车中数量不存在!"))

            # 判断库存是否足够
            if goods_sku.stock < count:
                return JsonResponse(json_msg(7, "库存不足!"))

            # 保存订单商品表
            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count
            )

            # 添加商品总金额
            goods_total_price += goods_sku.price * count

            # 扣除库存, 销量增加
            goods_sku.stock -= count
            goods_sku.sales += count
            goods_sku.save()

        # 3. 反过头来操作订单基本信息表 商品总金额 和 订单总金额
        # 订单总金额
        order_price = goods_total_price + transport.price
        order.goods_total_price = goods_total_price
        order.order_price = order_price
        order.save()

        # 4. 清空redis中的购物车数据(对应sku_id)
        r.hdel(cart_key, *sku_ids)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "创建订单成功!", data=order_sn))


class ShowOrder(JudgeSignIn):
    """确认支付页面"""

    def get(self, request):
        try:
            # 获取订单号，查订单和订单对应的商品
            order_sn = request.GET.get('order_sn')
            order = Order.objects.get(order_sn=order_sn)
            ordergoods = OrderGoods.objects.filter(order=order)
        except:
            return render(request, 'orders/order.html', context={'msg': '参数错误'})
        # 商品详情
        goodss = []
        for goods in ordergoods:
            goods_sku = GoodsSKUModel.objects.get(pk=goods.goods_sku_id, is_delete=False)
            goods_sku.count = goods.count
            goods_sku.totalprice = goods.price
            goodss.append(goods_sku)
        # 支付方式
        pay = Payment.objects.filter()
        context = {
            'order': order,
            'ordergoods': ordergoods,
            'goodss': goodss,
            'pay': pay,
        }
        return render(request, 'orders/order.html', context=context)


# 支付
class PayOrder(JudgeSignIn):
    def post(self, request):
        # 参数接收
        payment = request.POST.get('radio10')
        order_sn = request.POST.get('order_sn')
        user_id = request.session.get('id')

        # 判断参数合法性
        try:
            payment = int(payment)
        except:
            return JsonResponse(json_msg(1, "参数错误"))

        # 支付方式存在
        try:
            payment = Payment.objects.get(pk=payment)
        except Payment.DoesNotExist:
            return JsonResponse(json_msg(2, "支付方式不存在"))

        # 判断该订单是否是自己的, 并且是一个未支付的订单
        try:
            order = Order.objects.get(user_id=user_id, order_sn=order_sn, order_status=0)
        except Order.DoesNotExist:
            return JsonResponse(json_msg(3, "订单不满足要求"))

        # 判断 用户是否需要使用支付宝支付
        if payment.name == "支付宝":
            # 构造支付请求
            app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
            alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()

            # 初始化对象
            alipay = AliPay(
                appid="2016092400582019",
                app_notify_url=None,  # 默认回调url
                app_private_key_string=app_private_key_string,
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",  # RSA 或者 RSA2
                debug=True  # 默认False
            )

            # 构造请求地址
            order_string = alipay.api_alipay_trade_wap_pay(
                out_trade_no=order.order_sn,  # 订单编号
                total_amount=str(order.order_price),  # 订单金额
                subject="义乌超市订单支付",  # 订单描述
                return_url="http://127.0.0.1:8001/order/pay/",  # 同步通知地址
                notify_url=None  # 异步通知地址 重要
            )

            # 拼接地址
            url = "https://openapi.alipaydev.com/gateway.do?" + order_string

            # 通过json返回请求地址
            return JsonResponse(json_msg(0, "创建支付地址成功", data=url))
        else:
            return JsonResponse(json_msg(4, "该支付方式暂不支支持"))

    # 之前的post支付（）
    # def post(self, request):
    #     order_sn = request.POST.get('order_sn')
    #     radio10 = request.POST.get('radio10')
    #     try:
    #         order_sn = int(order_sn)
    #         radio10 = int(radio10)
    #     except:
    #         return JsonResponse(json_msg(1, '参数错误！'))
    #     # 支付时间
    #     now = datetime.now()
    #     try:
    #         # 支付方式
    #         payment = Payment.objects.get(pk=radio10)
    #     except:
    #         return JsonResponse(json_msg(2, '支付方式不存在！'))
    #     # 修改订单状态，支付方式，支付时间
    #     order = Order.objects.get(order_sn=order_sn)
    #     order.order_status = 1
    #     order.payment = payment
    #     order.pay_time = now
    #     order.save()
    #     return JsonResponse(json_msg(0, '支付成功！'))





class Pay(JudgeSignIn):
    """展示支付结果"""

    def get(self, request):

        # 查询订单是否交易成功
        # 构造支付请求
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()

        # 初始化对象
        alipay = AliPay(
            appid="2016092400582019",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 获取订单编号
        order_sn = request.GET.get('out_trade_no')
        total_amount = request.GET.get('total_amount')

        # check order status
        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        context = {
            'order_sn': order_sn,
            'total_amount': total_amount,
        }
        if paid is False:
            # 支付失败
            context['result'] = "支付失败"
        else:
            # 支付成功
            context['result'] = "支付成功"

        return render(request, "orders/pay.html", context=context)