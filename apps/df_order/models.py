from django.db import models

from df_goods.models import GoodsInfo
from df_user.models import UserInfo

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True, verbose_name="order_no")
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="order_users")
    odate = models.DateTimeField(auto_now=True, verbose_name="order_time")
    oIsPay = models.BooleanField(default=False, verbose_name="is_pay")
    ototal = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="total")
    oaddress = models.CharField(max_length=150,default='', verbose_name="order_address")
    oreceiver=models.CharField(max_length=20,default='',verbose_name='order_receiver')
    ocontact=models.CharField(max_length=11, default="", verbose_name="receiver_phone")


    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = verbose_name

    def __str__(self):

        return "{0}在的订单{1}".format(self.user.uname, self.odate)



class OrderDetailInfo(models.Model):

    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="products")
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="orders")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="goods_price")
    count = models.IntegerField(verbose_name="goods_count")

    class Meta:
        verbose_name = "order_details"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}(quantity{1})".format(self.goods.gtitle, self.count)