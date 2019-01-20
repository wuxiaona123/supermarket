# 引入继承
from django import forms

# 引入模型
from users.models import UserModels


# 验证注册
class RegisterForms(forms.ModelForm):
    # 密码
    password = forms.CharField(max_length=10,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码',
                                   'max_length': '密码最大长度为10位',
                                   'min_length': '密码最小长度为6位',
                               })
    # 确认密码
    repassword = forms.CharField(max_length=10,
                                 min_length=6,
                                 error_messages={
                                     'required': '请填写确认密码',
                                     'max_length': '确认密码最大长度为10位',
                                     'min_length': '确认密码最小长度为6位',
                                 })

    # 验证码
    yzm = forms.CharField(max_length=4,
                          min_length=4,
                          error_messages={
                              'required': '请填写验证码',
                              'max_length': '验证码为4个字符',
                              'min_length': '验证码为4个字符',
                          })



    # 验证电话号码
    class Meta:
        model = UserModels
        fields = ['phone']
        error_messages = {
            'phone': {
                'required': '请填写手机号码',
                'max_length': '手机号码格式错误',
                'min_length': '手机号码格式错误',
            }
        }

    # 再次验证手机号码，是否已经注册
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        ifexi = UserModels.objects.filter(phone=phone).exists()
        if ifexi:  # 数据库已经存在这个手机号码，不能让他注册
            forms.ValidationError('手机号码已经注册')
        else:   # 数据库不存在，可以让他继续注册
            return phone


    # 综合验证，验证两次密码是否一致
    def clean(self):
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['repassword']
        if password and repassword and password!=repassword:
            raise forms.ValidationError({'repassword':'两次密码不一致'})
        return self.cleaned_data
