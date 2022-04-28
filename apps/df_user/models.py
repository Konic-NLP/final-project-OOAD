from django.db import models

from datetime import datetime

from df_goods.models import GoodsInfo
# this defined two models, one if recording the user info, the other record the user view history

class UserInfo(models.Model):

    uname = models.CharField(max_length=20, verbose_name="user_nmae", unique=True)
    upwd = models.CharField(max_length=40, verbose_name="user_pwd", blank=False)
    uemail = models.EmailField(verbose_name="email")
    ushou = models.CharField(max_length=20, default="", verbose_name="shipping_address")
    uaddress = models.CharField(max_length=100, default="", verbose_name="address")
    ufullname=models.CharField(max_length=30, default="", verbose_name="full_name")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="zip_code")
    uphone = models.CharField(max_length=11, default="", verbose_name="phone_num")
    uanswer=models.CharField(max_length=30, default="", verbose_name="security_answer")
    uquestion = models.CharField(max_length=40, default="", verbose_name="security_question")


    class Meta:
        verbose_name = "User_Info"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname


class GoodsBrowser(models.Model):

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="user_ID")
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="goods_ID")
    browser_time = models.DateTimeField(default=datetime.now, verbose_name="browse_item")

    class Meta:
        verbose_name = "browser_history"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}view history{1}".format(self.user.uname, self.good.gtitle)
