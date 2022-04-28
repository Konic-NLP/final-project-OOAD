from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from .models import *
from df_user import user_decorator


@user_decorator.login
## The method decorator pattern is applied here.
## The method is wrapped by the login function to ensure that the user is logged in
## If the user is not logged in, the user will be redirected to the login page
## This method is used to display the shopping cart
def user_cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': 'Shopping Cart',
        'page_name': 1,
        'carts': carts
    }
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # How many items the current user purchased
        return JsonResponse({'count': count})
    else:
        return render(request, 'df_cart/cart.html', context)


@user_decorator.login
## The method decorator pattern is applied here.
## The method is wrapped by the login function to ensure that the user is logged in
## If the user is not logged in, the user will be redirected to the login page
## This method is used to add items to the shopping cart
def add(request, gid, count):
    uid = request.session['user_id']
    gid, count = int(gid), int(count)
    # Check if there is already this product in the shopping cart, if so, increase the quantity, if not, add it
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()

        return JsonResponse({'count': count})
    else:
        return redirect(reverse("df_cart:cart"))


@user_decorator.login
## The method decorator pattern is applied here.
## The method is wrapped by the login function to ensure that the user is logged in
## If the user is not logged in, the user will be redirected to the login page
## This method is used to modify the quantity of the shopping cart
def edit(request, cart_id, count):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data['count'] = 0
    except Exception:
        data['count'] = count
    return JsonResponse(data)


@user_decorator.login
## The method decorator pattern is applied here.
## The method is wrapped by the login function to ensure that the user is logged in
## If the user is not logged in, the user will be redirected to the login page
## This method is used to delete the items in the shopping cart
def delete(request, cart_id):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data['ok'] = 1
    except Exception:
        data['ok'] = 0
    return JsonResponse(data)
