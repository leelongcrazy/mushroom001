from django.db import models
from users.models import UserInfo


# from .untils import setDefaultUser


def setDefaultUser():
    """
    设置默认用户
    """
    user = UserInfo.objects.get(username='iisfree')
    return user


# 产品类型
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="产品类型")
    desc = models.TextField(verbose_name="产品类型描述")
    create_by = models.ForeignKey(to=UserInfo, related_name="category_creator", on_delete=models.PROTECT,
                                  default="", verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_by = models.ForeignKey(UserInfo, on_delete=models.PROTECT, verbose_name="更新人",
                                  default="", related_name="category_updater")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "产品类型"  # 类型
        verbose_name_plural = verbose_name
        db_table = "product_category"

    def __str__(self):
        return self.name


# 产品信息
class Product(models.Model):
    """"
    产品信息
    """
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='产品类型')
    name = models.CharField(max_length=128, verbose_name='设备名称', unique=True)
    desc = models.TextField(verbose_name='技术描述', blank=True, null=True)
    model = models.CharField(max_length=128, default='', verbose_name='型号')
    price = models.DecimalField(max_digits=50, decimal_places=2, verbose_name='面价')
    image = models.ImageField(max_length=128, upload_to='images/%Y/%m', default='/images/default.jpg',
                              verbose_name='产品图片')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_by = models.ForeignKey(UserInfo, on_delete=models.SET_DEFAULT, default="",
                                  verbose_name="创建人", related_name="product_creator")
    update_by = models.ForeignKey(UserInfo, on_delete=models.SET_DEFAULT, default="",
                                  verbose_name="更新人", related_name="product_updater")
    size = models.CharField(max_length=256, null=True, blank=True, verbose_name="设备尺寸")
    object_id = models.CharField(max_length=128, null=True, blank=True, verbose_name="料号")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name
        db_table = 'product_info'


# 订单产品信息
class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="单类型产品价格合计")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "订单产品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product} * {self.quantity}"


# 购物车
class Cart(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, through="CartItem")
    item_quantity = models.SmallIntegerField(default=0, verbose_name="产品种类数量")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user}的购物车"


# 购物车元素
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    # quantity = models.IntegerField(default=0)
    # cart_item_id = models.ForeignKey()

    class Meta:
        verbose_name = "购物车详细"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.cart} - {self.item} * {self.item.quantity}"


# 订单信息
class Order(models.Model):
    """
    订单详细信息
    """
    order_s = (
        (0, "报价中"),
        (1, "已下单"),
        (2, "已发货"),
        (3, "配送中"),
        (4, "退单"),
        (5, "完成"),
    )
    pay_s = (
        (0, "待支付"),
        (1, "未付清"),
        (2, "已支付"),
    )
    send_s = (
        (0, "备货中"),
        (1, "已发送"),
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    order_id = models.CharField(max_length=128, default='', verbose_name='订单编号', unique=True)
    create_by = models.ForeignKey(UserInfo, on_delete=models.SET_DEFAULT, verbose_name='创建人',
                                  default=setDefaultUser, related_name="order_creator")
    to_user = models.CharField(max_length=32, verbose_name='收货人')
    # products = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, verbose_name='订单产品')
    item = models.ManyToManyField(Item, through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="订单总价")
    order_status = models.SmallIntegerField(choices=order_s, default=0, verbose_name='订单状态')
    order_pay = models.SmallIntegerField(choices=pay_s, default=0, verbose_name='支付状态')
    order_send_status = models.SmallIntegerField(choices=send_s, default=0, verbose_name='发货状态')
    order_send_way = models.CharField(max_length=10, verbose_name='发货方式')
    order_send_nu = models.CharField(max_length=10, verbose_name='快递单号')
    update_by = models.ForeignKey(UserInfo, on_delete=models.SET_DEFAULT, verbose_name="更新人",
                                  default=setDefaultUser, related_name="order_updater")
    total_quantity = models.SmallIntegerField(default=0, verbose_name="订单总数量")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.order_id}"


# 订单元素
class OrderItem(models.Model):
    """
    关于订单的单品产品及数量
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0, verbose_name="产品数量")

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.order} - {self.item} * {self.quantity}"
