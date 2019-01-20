from django.conf.urls import url

from apps.shoppingcarts.views import Index

urlpatterns = [
    url(r'^$', Index.as_view(),name='index'),  # 购物车首页
]