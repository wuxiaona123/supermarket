import random
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# 引入发送短信需要的uuid
import uuid
# 引入发送短信的配置
from db.helper import send_sms
# 引入验证模型model forms
from users.forms import RegisterForms, LoginForms
# 引入模型
from users.models import UserModels
# 引入继承
from django.views import View
# 引入加密
from db.app_common import set_password


# 生成验证码
class Verification(View):
    def post(self, request):
        strs = ''.join([str(random.randint(0, 9)) for _ in range(4)])

        text = "您的验证码是：" + strs + "。请不要把验证码泄露给其他人。"
        print(text)
        data = request.POST.get('phone', '')
        m = re.findall(r'^1[34578]\d{9}$', data)
        if m:
            print(m)
            # 把验证码保存到ssesion
            request.session['verification'] = strs
            request.session.set_expiry(60)

            # 发送手机验证码
            __business_id = uuid.uuid1()
            params = "{\"code\":\"%s\"}" % text
            mysend = send_sms(__business_id, data, "用户注册验证码", "SMS_2245271", params)
            print(mysend.decode('utf-8'))
            return JsonResponse({"code": 1})
        else:
            return JsonResponse({"code": 2})


# 注册
class Register(View):
    def get(self, request):
        return render(request, 'users/reg.html')

    def post(self, request):
        data = request.POST.dict()
        verification = request.session.get('verification', '')
        data['verification'] = verification
        form = RegisterForms(data)
        if form.is_valid():
            cleane_data = form.cleaned_data
            password = set_password(cleane_data['password'])
            phone = cleane_data['phone']
            UserModels.objects.create(phone=phone, password=password)
            return redirect('users:login')
        else:
            context = {
                'form': form
            }
            return render(request, 'users/reg.html', context=context)


# 登录
class Login(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        data = request.POST
        form = LoginForms(data)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            request.session['id'] = user.pk
            request.session['user'] = user.phone
            return redirect('users:PersonalCenter ')
        else:
            context = {
                'form': form
            }
            return render(request, 'users/login.html', context=context)


# 个人中心
class PersonalCenter(View):
    def get(self, request):
        return render(request, 'users/member.html')

    def post(self, request):
        return HttpResponse('个人中心post')
