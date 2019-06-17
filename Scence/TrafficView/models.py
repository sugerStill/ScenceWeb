# Create your models here.
from django.db import models
'''城市交通数据库'''


# class DataBaseManager(models.Manager):
#     def get_quertset(self):
#         return super().get_queryset().filter()


# 城市交通主数据库
class MainCityTrafficDataBase(models.Model):
    name = models.CharField(max_length=32)
    # 根据pid可以确定其对应的所有表格---- 用于挖掘客流量
    cityCode = models.IntegerField(unique=True, verbose_name="城市ip")
    bounds_lon = models.FloatField()
    bounds_lat = models.FloatField()
    yearPid = models.IntegerField()

    class Meta:
        app_label = "TrafficView"
        db_table = "MainTrafficInfo"


class CityTraffic(models.Model):
    pid = models.ForeignKey(to='MainCityTrafficDataBase', on_delete=models.CASCADE,
                            verbose_name='城市交通ip', to_field='cityCode', related_name="CityTraffic")
    date = models.DateField(max_length=32, verbose_name="日期")  # 日期
    trafficindex = models.FloatField(verbose_name="交通拥堵指数")
    detailtime = models.CharField(max_length=16, verbose_name="时间点")

    class Meta:
        app_label = "TrafficView"
        db_table = 'CityTraffic'
        ordering = ['detailtime']


class RoadTraffic(models.Model):
    pid = models.ForeignKey(to='MainCityTrafficDataBase', on_delete=models.CASCADE,
                            verbose_name='城市道路交通ip', to_field='cityCode', related_name="RoadTraffic")
    date = models.DateField()  # 日期
    detailtime = models.CharField(max_length=32)  # 挖掘时间
    name = models.CharField(max_length=32)  # 路名
    direction = models.TextField()  # 具体道路方向
    speed = models.FloatField()  # 速度
    data = models.TextField()  # 拥堵数据
    bounds = models.TextField()  # 卫星数据
    flag = models.BooleanField()  # 判断数据是否失效，失效则用户无法访问

    class Meta:
        app_label = "TrafficView"
        ordering = ['speed']
        db_table = 'RoadTraffic'


class YearCityTraffic(models.Model):
    pid = models.ForeignKey(to='MainCityTrafficDataBase', on_delete=models.CASCADE,
                            verbose_name='城市季度交通ip', to_field='cityCode', related_name="YearTraffic")
    date = models.DateField()
    city = models.CharField(max_length=32)
    trafficindex = models.FloatField()

    class Meta:
        app_label = "TrafficView"
        db_table = 'YearCityTraffic'
        ordering = ['date']
