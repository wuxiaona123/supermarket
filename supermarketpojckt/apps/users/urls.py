from django.conf.urls import url
from apps.users.views import Register, Login, Verification, PersonalCenter, UserInfo, headimg

urlpatterns = [
    url(r'^$', Register.as_view(), name='register'),  # 注册
    url(r'^login/$', Login.as_view(), name='login'),  # 登录
    url(r'^verification/$', Verification.as_view(), name='verification'),  # 获取验证码
    url(r'^personalCenter/$', PersonalCenter.as_view(), name='PersonalCenter '),  # 个人中心
    url(r'^userInfo/$', UserInfo.as_view(), name='UserInfo '),  # 个人中心里面的    个人资料
    url(r'^headimg/$',headimg, name='headimg '),  # 上传头像
]
