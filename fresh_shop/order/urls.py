
from django.urls import path

from order import views

urlpatterns = [
    # 结算购物车
    path('place_order/', views.place_order, name='place_order'),
    # 创建订单
    path('order/', views.order, name='order'),

    path('user_order/', views.user_order, name='user_order'),


]