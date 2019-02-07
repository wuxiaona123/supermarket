from django.conf.urls import url

from apps.goods.views import Index, Category, Detail, AddReduceCar

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),   # 商品首页
    url(r'^category/(?P<classid>\d+)/(?P<sortgoods>\d)$', Category.as_view(), name='category'),  # 商品分类（商品列表）
    url(r'^detail/(?P<goodsid>\d+)$', Detail.as_view(), name='detail'),  # 商品详情
    url(r'^addreducecar/$', AddReduceCar.as_view(), name='addreducecar'),  # 加减购物车
]
