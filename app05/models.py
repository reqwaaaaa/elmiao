from django.db import models

# Create your models here.
class Student(models.Model):
    """用户信息表"""
    phone = models.CharField(verbose_name="联系电话", max_length=11)
    account = models.CharField(verbose_name="账号",max_length=20)
    password = models.CharField(verbose_name="密码",max_length=8)
    address = models.CharField(verbose_name="收货地址",max_length=50)
    balance = models.IntegerField(verbose_name="余额")
