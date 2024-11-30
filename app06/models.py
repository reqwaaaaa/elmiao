from django.db import models

# Create your models here.
class Order(models.Model):
    """订单信息表"""
    orderNum = models.CharField(verbose_name="订单号",max_length=15,default=None,unique=True)
    shopNum = models.CharField(verbose_name="商户编号", max_length=8)
    shopName = models.CharField(verbose_name="店铺名称",max_length=15)
    shopPhone = models.CharField(verbose_name="店铺联系电话",max_length=11)
    address0 = models.CharField(verbose_name="店铺地址", max_length=50)
    address1 = models.CharField(verbose_name="收货地址",max_length=50)
    stuPhone = models.CharField(verbose_name="收货人联系电话",max_length=11)
    note = models.CharField(verbose_name="订单备注",max_length=30)
    total = models.IntegerField(verbose_name="总计")
    status = models.BooleanField(verbose_name="订单状态",default=False)

class Foods(models.Model):
    orderNum = models.CharField(verbose_name="订单号", max_length=15,default=None)
    name = models.CharField(verbose_name="品名",max_length=15)
    num = models.IntegerField(verbose_name="数量")
    subtotal = models.IntegerField(verbose_name="小计")

class Eval(models.Model):
    """用户评价信息表"""
    shopNum = models.CharField(verbose_name="店铺编号", max_length=10,default=None)
    img = models.CharField(verbose_name="图片路径", max_length=50, default="")
    msg = models.CharField(verbose_name="评论文字内容",max_length=50)
    starNum = models.IntegerField(verbose_name="评分")