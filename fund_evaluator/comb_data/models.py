from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class CombData(models.Model):
    subAccountNo = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    passportID = models.CharField(max_length=100)
    AccountExistTime = models.CharField(max_length=100)
    AssetVol = models.CharField(max_length=100)
    drawdown = models.JSONField(null=True)
    sharpeRatio = models.JSONField(null=True)
    volatility = models.JSONField(null=True)
    earnDrawdownRatio = models.JSONField(null=True)
    compose = models.JSONField(null=True)
    user_fans_count = models.CharField(max_length=100)
    rise = models.JSONField(null=True)
    level = models.CharField(max_length=100,null=True)
    average_holding_days = models.CharField(max_length=10,null=True)

    def __str__(self):
        # return self.title 将文章标题返回
        return self.name
