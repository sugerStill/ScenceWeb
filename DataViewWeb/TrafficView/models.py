from django.db import models

# Create your models here.
from django.db import models

'''城市交通数据库'''

class DataBaseManager(models.Manager):
    def get_quertset(self):
        return super().get_queryset().filter(au)
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

class AuthRouter:
    def db_for_read(self, model, **hints):
        print(model)

        if model._meta.app_label=='TrafficView':
            return 'trafficdatabase'
        if model._meta.app_label=="webdata":
            return "webdata"
        return None

    def db_for_write(self, model, **hints):

        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'TrafficView':
            return 'trafficdatabase'
        if model._meta.app_label=="webdata":
            return "webdata"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        print(obj1,obj2)
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'TrafficView' or \
           obj2._meta.app_label == 'trafficdatabase':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(db)
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'TrafficView':
            return db == 'trafficdatabase'
        return None