# -*- coding: utf-8 -*-



def goods_recommend(user):
    pass

def load_data_set(user):

    """
    get_user_order
    :param user:
    :return:
     for example [['1', '2'], ['2', '34']]：
    """

    user_order_list = []
    for big_order in user.orderinfo_set.all():
        user_little_order_list = [str(good.goods.id) for good in big_order.orderdetailinfo_set.all()]
        user_order_list.append(user_little_order_list)

    data_set = user_order_list
    return data_set
