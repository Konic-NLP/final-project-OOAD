from datetime import datetime

from django.db import models
from tinymce.models import HTMLField  # 使用富文本编辑框要在settings文件中安装
# 将一对多的关系维护在GoodsInfo中维护，另外商品信息与分类信息都属于重要信息需要使用逻辑删除


class TypeInfo(models.Model):
    # 商品分类信息  水果 海鲜等
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="categories")

    class Meta:
        verbose_name = "product_category"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    # 具体商品信息
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    gtitle = models.CharField(max_length=20, verbose_name="goods_name", unique=True)
    gpic = models.ImageField(verbose_name='goods_pic', upload_to='df_goods/image/%Y/%m', null=True, blank=True)  # 商品图片
    # gpic = models.ImageField(upload_to="df_goods/image/%Y/%m", verbose_name="图片路径", default="image/default.png")
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="goods_price")  # 商品价格小数位为两位，整数位为3位
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
