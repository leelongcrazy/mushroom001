from django.urls import path, re_path

from .views import ProductView, CartView, AddCartView, OrdersView, OrderView

urlpatterns = [
    # 产品页面
    path('prod', ProductView.as_view(), name='prod'),
    # 购物车页面
    path('cart', CartView.as_view(), name='cart'),
    # 添加到购物车
    path('add_cart/<int:id>', AddCartView.as_view(), name='add_cart'),
    # 显示用户相关全部订单
    path('orders/', OrdersView.as_view(), name="orders_view"),
    # 显示订单详情
    path(r'order/<int:Oid>', OrderView.as_view(), name="order_view"),
]