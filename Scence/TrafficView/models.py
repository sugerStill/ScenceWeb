from django.db import models

# Create your models here.
from django.db import models

'''城市交通数据库'''

class DataBaseManager(models.Manager):
    def get_quertset(self):
        return super().get_queryset().filter()
    pass
# 城市交通主数据库
class MainCityTrafficDataBase(models.Model):
    name = models.CharField(max_length=32)
    # 根据pid可以确定其对应的所有表格---- 用于挖掘客流量
    cityCode = models.CharField(max_length=32)
    bounds_lon = models.FloatField()
    bounds_lat = models.FloatField()
    yearPid = models.IntegerField()
    class Meta:
        app_label="TrafficView"
        db_table="MainTrafficInfo"



class CityTraffic(models.Model):
    date = models.DateField(max_length=32)  # 日期
    data = models.FloatField()  # 拥堵指数
    time = models.CharField(max_length=16)  # 具体时间

    class Meta:
        abstract = True


class RoadTraffic(models.Model):
    date = models.DateField()  # 日期
    DetailTime = models.CharField(max_length=32)  # 挖掘时间
    name = models.CharField(max_length=32)  # 路名
    direction = models.TextField()  # 具体道路方向
    speed = models.FloatField()  # 速度
    data = models.TextField()  # 拥堵数据
    bounds = models.TextField()  # 卫星数据

    class Meta:
        abstract = True



class YearCityTraffic(models.Model):
    date = models.DateField()
    city = models.CharField(max_length=32)
    index = models.FloatField()
    class Meta:
        abstract = True
