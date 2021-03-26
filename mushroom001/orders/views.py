from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage  # 页面分页显示
from django.db.models import Q

import datetime
from decimal import Decimal

from .models import Product, Cart, Item, CartItem, OrderItem, Order
from users.models import UserInfo

from .untils import clean_form_data, toNum, genOrderId


# 产品展示
class ProductView(LoginRequiredMixin, View):
    login_url = '/login?redirect_to=prod'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'prod.html', locals())


# 购物车
class CartView(LoginRequiredMixin, View):
    login_url = '/login?redirect_to=cart'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        # items = dict()
        if not isinstance(request.user, (UserInfo,)):
            raise TypeError("user must be a UserInfo object")
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.cartitem_set.all()
            cart_sum = sum([item.item.quantity * item.item.price for item in items])
        except Cart.DoesNotExist:
            items = dict()
            cart_sum = 0
        return render(request, 'cart.html', locals())

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        items = clean_form_data(request.POST, {'ptn': r'product_(\d+)$', 'rpl': r'\1'}, del_val=())
        orders = clean_form_data(request.POST, {'ptn': r'order_product_(\d+)$', 'rpl': r'\1'})
        cart_items = cart.cartitem_set.all()
        products_id = [i.item.product.id for i in cart_items]

        # # 合并产品ID相同的cartItem
        # products_id_set = set(products_id)
        # resDict = dict()
        # for ele in products_id_set:
        #     id_index = [ i for i, x in enumerate(products_id) if x == ele]
        #     resDict[ele] = id_index
        #

        if "btn_save" in request.POST:
            try:
                for key in items:
                    item = cart_items.get(item=Item.objects.get(pk=toNum(key)))
                    if items[key] == 0:
                        item.delete()
                        Item.objects.filter(pk=toNum(key)).delete()
                    else:
                        if item.quantity != items[key]:
                            item.quantity = items[key]
                            item.update_time = datetime.datetime.now()
                            item.save()
                cart.save()
            except Exception as e:
                raise Http404("Something Error !!")

            if not isinstance(request.user, (UserInfo,)):
                raise TypeError("user must be a UserInfo object")
            try:
                cart = Cart.objects.get(user=request.user)
                items = cart.cartitem_set.all()
                for it in items:
                    post_quantity = request.POST.get('product_quantity_' + str(it.item_id))  # 获取保存修改后的数量值
                    if int(post_quantity) <= 0:  # 数量为0则删除
                        it.delete()
                    if it.item.quantity != post_quantity:
                        _item = Item.objects.get(id=it.item_id)
                        _item.quantity = post_quantity
                        _item.save()
                        it.item.quantity = post_quantity
                        # it.save()
                cart_sum = sum([Decimal(item.item.quantity) * item.item.price for item in items])
            except Cart.DoesNotExist:
                items = dict()
                cart_sum = 0
            message = ["success", "Cart saved."]
            return render(request, 'cart.html', locals())
        elif "btn_submit" in request.POST:
            if len(orders) > 0:
                order = Order.objects.create(create_by=request.user, total_price=0, order_id=genOrderId())
                for key in orders:
                    cartItem = cart_items.get(item=Item.objects.get(pk=toNum(key)))
                    OrderItem.objects.create(order=order, quantity=cartItem.item.quantity,
                                             item=Item.objects.get(pk=toNum(key)))
                    order.total_quantity += 1
                    order.total_price += cartItem.item.price * cartItem.item.quantity
                    cartItem.delete()
                order.save()
            # return render(request, 'orders.html', {'orders': Order.objects.filter(create_by=request.user),
            # 'message': None})
            return HttpResponseRedirect(reverse('orders_view'))


# 添加在购物车
class AddCartView(LoginRequiredMixin, View):
    login_url = '/login?redirect_to=add_cart'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        # product = Product.objects.get(id=id)
        product = get_object_or_404(Product, id=id)
        return render(request, 'add_cart.html', locals())

    def post(self, request, id):
        qty = toNum(request.POST['qty'])
        if qty is None or qty == 0:
            return HttpResponse("<script>window.close();</script>")

        # prepare cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        product = Product.objects.get(pk=id)
        item = Item(product=product, quantity=qty, price=product.price)
        item.save()
        # CartItem.objects.create(cart=cart, item=item, quantity=qty)

        try:
            cartItem = CartItem.objects.filter(Q(item__product_id=id) & Q(cart_id=cart.id))[0]
            if cartItem:
                # _item = Item.objects.filter(product_id=id).filter(cart__cartitem__item_id=cartItem.id)
                # _item.quantity += qty
                # _item.save()

                cartItem.item.quantity += qty
                cartItem.item.save()
            else:
                CartItem.objects.create(cart=cart, item=item)
            # cartItem.item.quantity += qty
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, item=item)
        except IndexError:
            CartItem.objects.create(cart=cart, item=item)
        return HttpResponseRedirect(reverse('cart'))


# 全部订单展示
class OrdersView(View):
    def get_orders_list(self, request):
        """
        返回所有订单的列表，并进行分页
        """
        order_list = Order.objects.filter(create_by=request.user).order_by()
        paginator = Paginator(order_list, 10)
        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except InvalidPage:
            raise Http404("Not Found.")
        return orders

    def get(self, request):
        orders = self.get_orders_list(request)
        return render(request, 'orders.html', locals())

    def post(self, request):
        deleteID = request.POST.get('delete')
        Order.objects.get(order_id=deleteID).delete()
        orders = self.get_orders_list(request)
        return render(request, 'orders.html', locals())


# 订单详情
class OrderView(View):
    def get(self, request, Oid):
        # print("print log", id)
        order = Order.objects.get(id=Oid)
        items = order.item.all()
        return render(request, 'order.html', locals())
