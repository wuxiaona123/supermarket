from django.conf.urls import url

from apps.goods.views import Index, Category, Detail

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),   # 商品首页
    url(r'^category/$', Category.as_view(), name='category'),  # 商品分类（商品列表）
    url(r'^detail/$', Detail.as_view(), name='detail'),  # 商品详情
]
