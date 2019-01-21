import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User, RecentBrowsing
from django.http import HttpResponseRedirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 拦截请求之前的函数
        # 1.给reuqest.user属性赋值，赋值为当前登录用户
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        # 登录校验，需区分哪些地址需要登录校验，哪些不需要登录校验
        path = request.path
        if path == '/':
            return None
        not_need_check = ['/user/register/', '/user/login/',
                          '/goods/index/', '/goods/detail/.*',
                          '/cart/.*/', '/media/.*/',
                          '/goods/list/', '/goods/list_price/',
                          '/goods/list_pop/', '/goods/search/',
                          ]
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path路径为不需要做登录校验的路由
                return None
        # 访问路由为需要登录的路由，判断登录状态，没有登录跳转到登录页面
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionToDbMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 同步session中de商品信息和数据库中购物车表的商品信息
        # 1.判断用户是否登录，登录才做数据同步操作
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 2.1 判断session中的商品是否存在于数据库中，如果存在，则同步，
            # 2.2 如果不存,在则创建
            # 2.3 同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=se_goods[0]).first()
                    if cart:
                        # 更新数据库的购物车商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 数据库创建购物车信息
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])
            # 同步数据库中的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            if db_carts:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id, cart.nums, cart.is_select]
                #     result.append(data)
        return response










