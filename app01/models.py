from django.db import models

# Create your models here.
class Manager(models.Model):
    """管理员信息表"""
    employeeNum = models.CharField(verbose_name="工号",max_length=8)
    name = models.CharField(verbose_name="姓名",max_length=15)
    gender = models.CharField(verbose_name="性别",max_length=1)
    age = models.IntegerField(verbose_name="年龄")
    password = models.CharField(verbose_name="密码",max_length=8)
