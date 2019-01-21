from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Goods, GoodsCategory
from user.models import RecentBrowsing


def index(request):
    if request.method == 'GET':
        # 如果访问首页，渲染index.html页面并返回
        # 思路组装结果[objects1,objects2,objects3,objects4,objects5,objects6]
        # 组装结果的对象object：包括：分类的前四个商品信息
        # 方式1：[GoodsCategory Object,[Goods Object1,Goods Object2,Goods Object3,Goods Object4]]
        # 方式2：{GoodsCategory_name:[Goods Object1,Goods Object2,Goods Object3,Goods Object4]}
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result,
                                              'category_type': category_type})
        # return render(request, 'index.html')


# 商品详情（新增商品人气排行（点击量），需要重写，以及历史记录的本地同步和去重，以及控制条数）
def detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        click_num = goods.click_nums
        goods.click_nums = click_num + 1
        goods.save()
        user_id = request.session.get('user_id')
        if user_id:
            RecentBrowsing.objects.create(user_id=user_id, details=id)
        return render(request, 'detail.html', {'goods': goods})
    if request.method == 'POST':
        pass


def list1(request):
    act1 = True
    if request.method == 'GET':
        all_goods = Goods.objects.all()
        page = int(request.GET.get('page', 1))
        pg = Paginator(all_goods, 10)
        all_goods = pg.page(page)
        return render(request, 'list.html', {'all_goods': all_goods, 'act1':act1})


# 商品搜索（bug）
def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('key')
        if keyword:
            the_category = GoodsCategory.objects.filter(category_name__contains=keyword).all()
            all_goods = Goods.objects.filter(name__contains=keyword).all()
            if the_category:
                all_goods = []
                for x in the_category:
                    cate_id = x.id
                    print(cate_id)
                    the_goods = Goods.objects.filter(category_id=cate_id)
                    for goods in the_goods:
                        all_goods.append(goods)
                return render(request, 'list.html', {'all_goods': all_goods})
            elif all_goods:
                print('=====', all_goods)
                return render(request, 'list.html', {'all_goods': all_goods})
            else:
                msg = '没有找到任何商品'
                return render(request, 'list.html', {'msg': msg})


def list_price(request):
    act2 = True
    if request.method == 'GET':
        all_goods = Goods.objects.all().order_by('-shop_price')
        page = int(request.GET.get('page', 1))
        pg = Paginator(all_goods, 10)
        all_goods = pg.page(page)
        return render(request, 'list.html', {'all_goods': all_goods, 'act2': act2})


def list_pop(request):
    act3 = True
    if request.method == 'GET':
        all_goods = Goods.objects.all().order_by('-click_nums')
        page = int(request.GET.get('page', 1))
        pg = Paginator(all_goods, 10)
        all_goods = pg.page(page)
        return render(request, 'list.html', {'all_goods': all_goods, 'act3': act3})
