"""supermarketpojckt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),  # 上传部件自动调用的上传地址
    url(r'^user/', include('apps.users.urls', namespace='users')),  # 用户app
    url(r'^', include('apps.goods.urls', namespace='goods')),  # 商品app
    url(r'^shoppingcart/', include('apps.shoppingcarts.urls', namespace='shoppingcart')),  # 购物车app
    url(r'^orders/', include('apps.orders.urls', namespace='orders')),  # 订单app
]
