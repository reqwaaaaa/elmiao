from django.db import models

# Create your models here.
class Shop(models.Model):
    """商家表"""
    enterData = models.DateTimeField(verbose_name="入驻日期")
    shopNum = models.CharField(verbose_name="商户编号", max_length=8,unique=True)
    name = models.CharField(verbose_name="店铺管理者姓名", max_length=15)
    legalPerson = models.CharField(verbose_name="法人姓名", max_length=15,default="")
    phoneNum = models.CharField(verbose_name="联系电话", max_length=11)
    address = models.CharField(verbose_name="店铺地址", max_length=50)
    password = models.CharField(verbose_name="密码",max_length=10, default="")
    img = models.CharField(verbose_name="图片路径", max_length=50, default="")
    sale = models.IntegerField(verbose_name="每日销售额", default=0)
    main = models.IntegerField(verbose_name="主营", default=1)

class Food(models.Model):
    """食物信息表"""
    shopNum = models.CharField(verbose_name="所属商铺编号",max_length=8,default=None)
    name = models.CharField(verbose_name="食物名称",max_length=20)
    explain = models.CharField(verbose_name="食物介绍",max_length=35)
    img = models.CharField(verbose_name="图片路径",max_length=50,default="")
    price = models.IntegerField(verbose_name="单价")
    sellOut = models.BooleanField(verbose_name="是否售罄",default=False)





