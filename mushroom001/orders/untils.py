#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2021/3/15 15:30
    Author  : leelongcrazy
    File    : untils.py
    Software: PyCharm
    Description:
"""
import re
from datetime import datetime
from orders.models import Cart
from users.models import UserInfo

ORDER_COUNT = 1


def clean_form_data(form_data, key_ptn={'ptn': r'topping_(\d+)$', 'rpl': r'\1'}, del_val=("", "0")):
    """Clean form data POST
    """
    o = dict()
    for key in form_data:
        try:
            if re.match(key_ptn['ptn'], key) and form_data[key][0] not in del_val:
                o[re.sub(key_ptn['ptn'], key_ptn['rpl'], key)] = int(form_data[key][0])
        except:
            pass
    return(o)

def toNum(txt):
    """
    将文本转换为数字类型
    """
    if not txt:
        return None
    elif txt.isdigit():
        return int(txt)
    else:
        try:
            return float(txt)
        except ValueError:
            return None

def showCart(user):
    if not isinstance(user, (,)):
        raise TypeError("user must be a UserInfo object")
    try:
        cart = Cart.objects.get(user=user)
        items = cart.cartitem_set.all()
        cart_sum = sum([item.quantity * item.item.price for item in items])
    except Cart.DoesNotExist:
        items = dict()
        cart_sum = 0
    return {'items': items, 'cart_sum': cart_sum}

def genOrderId():
    """
    生成订单号
    """
    global ORDER_COUNT
    base_code = datetime.now().strftime("%Y%m%d%H%M%S")
    count_str = str(ORDER_COUNT).zfill(6)
    ORDER_COUNT += 1
    return base_code+count_str


if __name__ == '__main__':
    for i in range(100):
        print(genOrderId())