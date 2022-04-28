from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse

from datetime import datetime
from decimal import Decimal

from .models import OrderInfo, OrderDetailInfo
from df_cart.models import CartInfo
from df_user.models import UserInfo
from df_user import user_decorator


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
    trans_cost = 10  # shipping fee
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
@transaction.atomic()
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.POST.get('cart_ids')
    user_id = request.session['user_id']
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

        for cart_id in cart_ids.split(','):
            cart = CartInfo.objects.get(pk=cart_id)
            order_detail = OrderDetailInfo()
            order_detail.order = order_info
            goods = cart.goods
            if cart.count <= goods.gkucun:
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
