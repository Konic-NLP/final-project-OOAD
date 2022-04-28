from datetime import datetime

from django.db import models
from tinymce.models import HTMLField



class TypeInfo(models.Model):
    # Product type
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="categories")

    class Meta:
        verbose_name = "product_category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


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
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="category")
    # gadv = models.BooleanField(default=False)

    class Meta:
        verbose_name = "products"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle
