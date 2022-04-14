from django.db import models

from df_goods.models import GoodsInfo
from df_user.models import UserInfo

class OrderInfo(models.Model):  # 大订单
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="order_no")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="order_users")
    odate = models.DateTimeField(auto_now=True, verbose_name="order_time")
    oIsPay = models.BooleanField(default=False, verbose_name="is_pay")
    ototal = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="total")
    oaddress = models.CharField(max_length=150, verbose_name="order_address")
    # 虽然订单总价可以由多个商品的单价以及数量求得，但是由于用户订单的总价的大量使用，忽略total的冗余度

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.user.uname + "在" + str(self.odate) + "的订单"
        return "{0}在的订单{1}".format(self.user.uname, self.odate)


# 无法实现：真实支付，物流信息
class OrderDetailInfo(models.Model):  # 大订单中的具体某一商品订单

    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="products")  # 关联商品信息
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="orders")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="goods_price")
    count = models.IntegerField(verbose_name="goods_count")

    class Meta:
        verbose_name = "order_details"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.goods.gtitle + "(数量为" + str(self.count)  + ")"
        return "{0}(数量为{1})".format(self.goods.gtitle, self.count)