from django.conf.urls import url

from apps.users.views import Register, Login, Verification, PersonalCenter

urlpatterns = [
    url(r'^$', Register.as_view(), name='register'),  # 注册
    url(r'^login/$', Login.as_view(), name='login'),  # 登录
    url(r'^verification/$', Verification .as_view(), name='verification '),  # 获取验证码
    url(r'^PersonalCenter/$', PersonalCenter .as_view(), name='PersonalCenter '),  # 获取验证码
]
