from django.db import models

# Create your models here.
class Worker(models.Model):
    """外卖员信息表"""
    employeeNum = models.CharField(verbose_name="工号", max_length=8)
    name = models.CharField(verbose_name="姓名", max_length=15)
    phoneNum = models.CharField(verbose_name="联系电话",max_length=11)
    gender = models.CharField(verbose_name="性别", max_length=1)
    salary = models.IntegerField(verbose_name="工资")


