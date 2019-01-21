from django.conf import settings
import hashlib
from django.shortcuts import redirect


# 加密  用 setting  中的   SECRET_KEY  加盐
def set_password(password):
    strs = '{}{}'.format(password, settings.SECRET_KEY)
    h = hashlib.md5(strs.encode('utf-8'))
    return h.hexdigest()


# 判断登录的装饰器
def judgeSignIn(fun):
    def new_fun(request, *args, **kwargs):
        user = request.session.get('user', '')
        if user == '':
            return redirect('users:login')
        else:
            return fun(request, *args, **kwargs)
    return new_fun
