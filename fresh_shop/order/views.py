from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.function import get_order_sn


def place_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        address = UserAddress.objects.filter(user_id=user_id).all()
        # 获取当前登录系统的用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        # 计算小计和总价
        total_price = 0
        count = len(carts)
        for cart in carts:
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            total_price += price

        return render(request, 'place_order.html',
                      {'carts': carts, 'total_price': total_price, 'count': count, 'address': address})


def order(request):
    if request.method == 'POST':
        # 获取用户id
        user_id = request.session.get('user_id')
        # 1.获取收货地址id值
        ad_id = request.POST.get('ad_id')
        print(ad_id)
        # 获取地址详情
        i = UserAddress.objects.filter(pk=ad_id).first()
        # 获取购物车详情
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,
                                                is_select=True)
        # 总金额
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums
        # 获取订单号
        order_sn = get_order_sn()
        # 2.创建订单
        order = OrderInfo.objects.create(user_id=user_id, order_sn=order_sn,
                                         order_mount=order_mount, address=i.address,
                                         signer_name=i.signer_name, signer_mobile=i.signer_mobile)
        # 3.生成订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4.删除购物车信息
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods[:]:
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_order(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        user_id = request.session.get('user_id')
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        return render(request, 'user_center_order.html',
                      {'orders': orders, 'status': status})
