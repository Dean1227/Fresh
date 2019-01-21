
from django.urls import path

from user import views

urlpatterns = [
    # 注册
    path('register/', views.register, name='register'),
    # 登录
    path('login/', views.login, name='login'),
    # 退出
    path('logout/', views.logout, name='logout'),

    path('user_center_site/', views.user_center_site, name='user_center_site'),

    path('user_info/', views.user_info, name='user_info'),
]