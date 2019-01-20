from django.conf.urls import url

from apps.users.views import Register, Login

urlpatterns = [
    url(r'^$', Register.as_view(), name='register'),  # 注册
    url(r'^login/$', Login.as_view(), name='login'),  # 登录
]
