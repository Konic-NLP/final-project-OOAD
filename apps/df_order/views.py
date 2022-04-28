from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse

from datetime import datetime
from decimal import Decimal

from .models import OrderInfo, OrderDetailInfo
from df_cart.models import CartInfo
from df_user.models import UserInfo
from df_user import user_decorator
from abc import ABC,abstractmethod


class Strategy(ABC):
    @abstractmethod
    def calculate(self):
        pass

class freestrategy(Strategy):
    def calculate(self):
        return 0
class normalstrategy(Strategy):
    def calculate(self):

        return 10

class Shippingfee:
    strategy:Strategy
    def __init__(self,price,strategy):
        self.price=price
        self.strategy=strategy
    def calculate(self):
        shipcost =self.strategy.calculate()
        return shipcost



@user_decorator.login
def order(request):
    uid = request.session['user_id']
    # user = UserInfo.objects.get(id=uid)
    latest=OrderInfo.objects.filter(user_id=uid)
    receiver=latest.order_by('-oid')[0]
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    total_price = 0
    for goods_id in cart_ids:
        cart = CartInfo.objects.get(id=goods_id)
        carts.append(cart)
        total_price = total_price + float(cart.count) * float(cart.goods.gprice)

    total_price = float('%0.2f' % total_price)
    trans_cost=0
    if total_price>50:
        shipping = Shippingfee(total_price,freestrategy())
        trans_cost=shipping.calculate()
    else:
        shipping =Shippingfee(total_price,normalstrategy())
        trans_cost=shipping.calculate()
    # trans_cost = 10  # 运费
    total_trans_price = trans_cost + total_price
    context = {
        'title': '提交订单',
        'page_name': 1,
        'user': receiver,
        'carts': carts,
        'total_price': float('%0.2f' % total_price),
        'trans_cost': trans_cost,
        'total_trans_price': total_trans_price,
        # 'value':value
    }
    return render(request, 'df_order/place_order.html', context)


@user_decorator.login
@transaction.atomic()  # 事务
def order_handle(request):
    tran_id = transaction.savepoint()  # 保存事务发生点
    cart_ids = request.POST.get('cart_ids')  # 用户提交的订单购物车，此时cart_ids为字符串，例如'1,2,3,'
    user_id = request.session['user_id']  # 获取当前用户的id
    address=request.POST.get('address')
    receiver=request.POST.get('receiver')
    phone = request.POST.get('contact')
    data = {}
    try:
        order_info = OrderInfo()  # create an order object
        now = datetime.now()
        # order number is the combination of order time and user id
        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)
        order_info.odate = now  # order time
        order_info.user_id = int(user_id)  # user id
        order_info.ototal = Decimal(request.POST.get('total'))  # get total from the front end
        order_info.oaddress=address
        order_info.ocontact=phone
        order_info.oreceiver=receiver
        order_info.save()  # save order

        for cart_id in cart_ids.split(','):  # 逐个对用户提交订单中的每类商品即每一个小购物车
            cart = CartInfo.objects.get(pk=cart_id)  # 从CartInfo表中获取小购物车对象
            order_detail = OrderDetailInfo()  # 大订单中的每一个小商品订单
            order_detail.order = order_info  # 外键关联，小订单与大订单绑定
            goods = cart.goods  # 具体商品
            if cart.count <= goods.gkucun:  # 判断库存是否满足订单，如果满足，修改数据库
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.save()
                cart.delete()  # delete current cart
            else:
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('Out of Stock')
        data['ok'] = 1
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("%s" % e)
        print('Place order failed')
        transaction.savepoint_rollback(tran_id)
    return JsonResponse(data)


@user_decorator.login
def pay(request):
    pass
