import random
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# 引入发送短信需要的uuid
import uuid
# 引入发送短信的配置
from db.helper import send_sms
# 引入验证模型model forms
from users.forms import RegisterForms, LoginForms, SetPasswordForm
# 引入模型
from users.models import UserModels
# 引入继承
from django.views import View
# 引入加密
from db.app_common import set_password
# 引入基础视图，判断是否登录
from db.base_view import JudgeSignIn
# 上传头像没有csrf
from django.views.decorators.csrf import csrf_exempt


# 生成验证码
class Verification(View):
    def post(self, request):
        try:
            # 获取手机号码
            phone = request.POST.get('phone')
            # 验证手机号是否正确
            phone_re = re.compile('^1[3-9]\d{9}$')
            res = re.search(phone_re, phone)
            if res:
                # 生成随机验证码
                code = "".join([str(random.randint(0, 9)) for _ in range(4)])
                print(code)
                print("===========================")
                # 把验证码保存到ssesion
                request.session['verification'] = code
                request.session.set_expiry(60)
                # 发送短信验证码
                __business_id = uuid.uuid1()
                # 信息
                params = "{\"code\":\"%s\",,\"product\":\"吴娟的测试短信\"}" % code
                rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
                print(rs.decode('utf-8'))
                return JsonResponse({'ok': 1, 'code': 200})
            else:
                return JsonResponse({'ok': 0, 'code': 500, 'msg': '手机号码格式错误！'})
        except:
            return JsonResponse({'ok': 0, 'code': 500, 'msg': '短信验证码发送失败'})


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
            return redirect('users:PersonalCenter')
        else:
            context = {
                'form': form
            }
            return render(request, 'users/login.html', context=context)


# 个人中心
class PersonalCenter(JudgeSignIn):
    def get(self, request):
        return render(request, 'users/member.html')

    def post(self, request):
        return render(request, 'users/member.html')


# 个人资料
class UserInfo(JudgeSignIn):
    def get(self, request):
        getid = request.session.get('id')
        user = UserModels.objects.filter(id=getid).first()
        context = {
            'user': user
        }
        return render(request, 'users/infor.html', context=context)

    def post(self, request):
        data = request.POST
        getid = request.session.get('id')
        user = UserModels.objects.filter(id=getid)
        user.update(nickname=data['nickname'],
                    gender=data['gender'],
                    birthday=data['birthday'],
                    school=data['school'],
                    address=data['address'],
                    hometown=data['hometown'],
                    )

        context = {
            'user': user.first()
        }
        return render(request, 'users/infor.html', context=context)


# 上传头像
@csrf_exempt
def headimg(request):
    user = UserModels.objects.get(pk=request.session.get("id"))
    user.head = request.FILES['file']
    user.save()
    return JsonResponse({"status": "ok", "head": str(user.head)})


# 安全设置
class Saftystep(JudgeSignIn):
    def get(self, request):
        return render(request, 'users/saftystep.html')


# 修改密码
class SetPassword(JudgeSignIn):
    def get(self, request):
        return render(request, 'users/password.html')

    def post(self, request):
        data = request.POST
        userid = request.session.get('id')
        datas=data.dict()
        datas['userid']=userid
        form = SetPasswordForm(datas)
        if form.is_valid():
            context = {
                'sec': '修改成功'
            }
            return render(request, 'users/password.html', context=context)
        else:
            context = {
                'formdata': form
            }
            return render(request, 'users/password.html', context=context)
