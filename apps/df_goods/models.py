from datetime import datetime

from django.db import models
from tinymce.models import HTMLField

# record the information of the category for each products

class TypeInfo(models.Model):
    # Product type
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="categories")

    class Meta:
        verbose_name = "product_category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle
#  

class GoodsInfo(models.Model):
    # product details
    isDelete = models.BooleanField(default=False)
    gtitle = models.CharField(max_length=20, verbose_name="goods_name", unique=True)
    gpic = models.ImageField(verbose_name='goods_pic', upload_to='df_goods/image/%Y/%m', null=True, blank=True)  # img
    # gpic = models.ImageField(upload_to="df_goods/image/%Y/%m", verbose_name="img path", default="image/default.png")
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="goods_price")
    gunit = models.CharField(max_length=20, default='500g', verbose_name="unit_weight")
    gclick = models.IntegerField(verbose_name="click_count", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="short_inro")
    gkucun = models.IntegerField(verbose_name="stock", default=0)
    gcontent = HTMLField(max_length=200, verbose_name="descriptions")
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="category")  # 外键关联TypeInfo表
    # gadv = models.BooleanField(default=False) #商品是否推荐

    class Meta:
        verbose_name = "products"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle
#this is a Proxy pattern, which  is a proxy of the goodsinfo, the proxy change the order way of the original models while not impact the original models,  the client can extract  model
# can extract information from goosinfo via proxy while cannot change the goodsinfo

class GoodsinfoProxy(GoodsInfo):
    class Meta:
        ordering=['-id']
        proxy=True

