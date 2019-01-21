
from django.urls import path

from goods import views

urlpatterns = [
    # 首页
    path('index/', views.index, name='index'),
    # 详情
    path('detail/<int:id>', views.detail, name='detail'),
    # 默认列表
    path('list/', views.list1, name='list'),
    # 搜索
    path('search/', views.search, name='search'),
    # 价格
    path('list_price/', views.list_price, name='list_price'),
    # 人气
    path('list_pop/', views.list_pop, name='list_pop'),


]