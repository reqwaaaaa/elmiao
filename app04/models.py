from django.db import models

# Create your models here.
class Notice(models.Model):
    """通知表"""
    msg = models.CharField(verbose_name="通知内容",max_length=50)

