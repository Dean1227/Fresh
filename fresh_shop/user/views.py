from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from goods.models import Goods
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress, RecentBrowsing


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 使用表单form做校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 满足注册条件，向数据库中添加用户信息
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                                password=password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单校验不过的错误信息，并返回页面
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 登录验证通过跳转到页面首页
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            # 获取表单校验不过的错误信息，并返回页面
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        del request.session['user_id']
        if request.session.get('goods'):
            del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))


def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id).all()
        return render(request, 'user_center_site.html', {'user_address': user_address})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})


def user_info(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        r_browser = RecentBrowsing.objects.filter(user_id=user_id).all()
        if r_browser:
            r_goods = []
            for x in r_browser[::-1]:
                detail = int(x.details)
                if detail:
                    goods = Goods.objects.filter(id=detail).first()
                    r_goods.append(goods)
                    print(r_goods)
                    if len(r_goods) > 5:
                        r_goods = r_goods[0:5]
            return render(request, 'user_center_info.html', {'r_goods': r_goods})
        else:
            return render(request, 'user_center_info.html')