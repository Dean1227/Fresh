import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):

    user_name = forms.CharField(max_length=20, min_length=5, required=True,
                                error_messages={'required': '用户名必填',
                                                'max_length': '最大长度为20',
                                                'min_length': '最小长度为5'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '密码名必填',
                                          'max_length': '最大长度为20',
                                          'min_length': '最小长度为8'})
    cpwd = forms.CharField(max_length=20, min_length=8, required=True,
                           error_messages={'required': '密码名必填',
                                           'max_length': '最大长度为20',
                                           'min_length': '最小长度为8'})
    email = forms.CharField(required=True,
                            error_messages={'required': '邮箱必填'})
    allow = forms.CharField(required=True,
                            error_messages={'required': '必须同意协议'})

    def clean_user_name(self):
        # 校验注册的账号是否存在
        username = self.cleaned_data['user_name']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已存在，请更换用户名重新注册')
        return self.cleaned_data['user_name']

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

    def clean_email(self):
        email_reg = r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_reg, email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True)
    pwd = forms.CharField(max_length=20, min_length=8, required=True)

    def clean(self):
        # 校验用户名是否已经注册
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号未注册，请注册'})
        password = self.cleaned_data.get('pwd')
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5,required=True,
                               error_messages={'required': '收件人必填',
                                               'max_length': '最大长度为5'})
    address = forms.CharField(required=True, error_messages={'required': '收货地址必填'})
    postcode = forms.CharField(required=True, error_messages={'required': '邮编必填'})
    mobile = forms.CharField(required=True, error_messages={'required': '手机号必填'})

    def clean(self):
        pass



