from django.http import HttpResponse
from django.shortcuts import render
# 引入验证模型model forms
from users.forms import RegisterForms

# 引入继承
from django.views import View
#     # todo:checkbox 是否同意用户协议（先不验证）
## todo:头像还没建



class Register(View):
    def get(self, request):
        return render(request, 'users/reg.html')

    def post(self, request):
        data = request.POST
        # print(data['checkbox'])
        #
        form = RegisterForms(data)
        # if form.is_valid():
        #     cleane_data = form.cleaned_data
        #     return HttpResponse('注册验证正确')
        # else:
        #     return render(request, 'users/reg.html', context=form)
        return HttpResponse('注册post')


# 登录
class Login(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        return HttpResponse('登录post')
