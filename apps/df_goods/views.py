from django.core.paginator import Paginator
from django.shortcuts import render

from df_user.models import UserInfo
from .models import GoodsInfo, TypeInfo,GoodsinfoProxy
from df_cart.models import CartInfo
from df_user.models import GoodsBrowser


def index(request):
    # check the 4 new arrival product of category
    typelist = TypeInfo.objects.all()
    goodsinfo=GoodsInfo.objects.all()

    type=goodsinfo.order_by('-id')[:8]
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:8]  # according to new arrival
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:8]  #according to clicks
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:8]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:8]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:8]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:8]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:8]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:8]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:8]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:8]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:8]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:8]

    type100 = goodsinfo.order_by('-gclick')[:8]

    cart_num = 0
    # check if login
    # if request.session.has_key('user_id'):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': 'HOME',
        'cart_num': cart_num,
        'guest_cart': 1,

        'type0': type, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
        'type100': type100
    }

    return render(request, 'df_goods/index.html', context)


def good_list(request, tid, pindex, sort):
    # tid：product type info  pindex：product page sort：how product display
    typeinfo = TypeInfo.objects.get(pk=int(tid))

    # inquiry the current product category base on the primary key
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    goods_list = []

    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    if sort == '1':  # default(from the newest)
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # price
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # hot
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # Paginator
    paginator = Paginator(goods_list, 10)
    # return page object
    page = paginator.page(int(pindex))
    context = {
        'title': 'Product List',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'news': news,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    good_id = gid
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.gclick = goods.gclick + 1  #clicks
    goods.save()

    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': goods.gtype.ttitle,
        'guest_cart': 1,
        'cart_num': cart_count(request),
        'goods': goods,
        'news': news,
        'id': good_id,
    }
    response = render(request, 'df_goods/detail.html', context)

    if 'user_id' in request.session:
        user_id = request.session["user_id"]
        try:
            browsed_good = GoodsBrowser.objects.get(user_id=int(user_id), good_id=int(good_id))
        except Exception:
            browsed_good = None
        if browsed_good:
            from datetime import datetime
            browsed_good.browser_time = datetime.now()
            browsed_good.save()
        else:
            GoodsBrowser.objects.create(user_id=int(user_id), good_id=int(good_id))
            browsed_goods = GoodsBrowser.objects.filter(user_id=int(user_id))
            browsed_good_count = browsed_goods.count()
            if browsed_good_count > 5:
                ordered_goods = browsed_goods.order_by("-browser_time")
                for _ in ordered_goods[5:]:
                    _.delete()
    return response


def cart_count(request):
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count
    else:
        return 0


def ordinary_search(request):

    from django.db.models import Q

    search_keywords = request.GET.get('q', '')
    pindex = request.GET.get('pindex', 1)
    search_status = 1
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None

    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    goods_list = GoodsInfo.objects.filter(
        Q(gtitle__icontains=search_keywords) |
        Q(gcontent__icontains=search_keywords) |
        Q(gjianjie__icontains=search_keywords)).order_by("gclick")

    if goods_list.count() == 0:
        # search result is empty, return some recommendation
        search_status = 0
        goods_list = GoodsInfo.objects.all().order_by("gclick")[:4]

    paginator = Paginator(goods_list, 4)
    page = paginator.page(int(pindex))

    context = {
        'title': 'Search list',
        'search_status': search_status,
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'query':search_keywords
    }
    return render(request, 'df_goods/ordinary_search.html', context)
