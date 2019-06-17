'''景区数据库'''

from django.db import models


class JingQuDatabase(models.Model):
    id = models.AutoField(primary_key=True, unique=True)

    name = models.CharField(max_length=32, verbose_name="景区名字")

    # 根据pid可以确定其对应的所有表格---- 用于挖掘客流量
    #     #   地理位置
    bounds_lon = models.FloatField(verbose_name="经纬度")
    bounds_lat = models.FloatField(verbose_name="经纬度")
    PeoplePid = models.IntegerField(verbose_name="景区ip")
    CityCode = models.IntegerField(verbose_name="城市交通ip", default=0)
    WeatherPid = models.CharField(max_length=32, verbose_name="天气情况ip")
    PeopleTablePid = models.IntegerField(unique=True, verbose_name="景区表")
    CityTableCode = models.IntegerField(unique=True, verbose_name="城市交通表")
    WeatherTablePid = models.IntegerField(max_length=32, unique=True, verbose_name="天气情况表")

    class Meta:
        db_table = "ScenceInfoData"
        app_label = 'ScenceView'

    @property
    def info(self):
        return "%s %d" % (self.name, self.PeoplePid)


class PeopleFlow(models.Model):

    def get(self, item):
        return self.__dict__.get(item)

    pid = models.ForeignKey(to='JingQuDatabase', on_delete=models.CASCADE, verbose_name="景区pid",
                            to_field='PeopleTablePid', related_name="Flow")
    date = models.DateField(verbose_name="日期")  # 日期
    num = models.IntegerField(verbose_name="客流")
    detailTime = models.CharField(max_length=16, verbose_name="时间点")

    class Meta:
        db_table = "peopleFlow"

        ordering = ['detailTime']
        indexes = [
            models.Index(fields=['pid'], name="ScencePid"),
            models.Index(fields=['date'], name='Day')
        ]

        app_label = 'ScenceView'


#
class Traffic_Data(models.Model):
    pid = models.ForeignKey(to='JingQuDatabase', on_delete=models.CASCADE, to_field='CityTableCode',
                            verbose_name="景区pid", related_name="Traffic")
    date = models.DateField(max_length=32, verbose_name="日期")  # 日期
    TrafficIndex = models.FloatField(verbose_name="交通拥堵指数")
    detailTime = models.CharField(max_length=16, verbose_name="时间点")

    def get(self, item):
        return self.__dict__.get(item)

    class Meta:
        db_table = "traffic"
        ordering = ['detailTime']
        indexes = [models.Index(fields=['pid'], name='景区pid'),
                   models.Index(fields=['date'], name='Day')]
        app_label = 'ScenceView'


# # # 模板表
#
class Weather_Data(models.Model):
    pid = models.ForeignKey(to='JingQuDatabase', on_delete=models.CASCADE, to_field='WeatherTablePid',
                            verbose_name="景区pid", related_name="weather")
    date = models.DateField(max_length=32, verbose_name="日期")
    detailTime = models.CharField(max_length=16, verbose_name="时间点")

    state = models.CharField(max_length=32, verbose_name="天气状态")
    temperature = models.CharField(max_length=16, verbose_name="气温")
    wind = models.CharField(max_length=32, verbose_name='风力风向')

    class Meta:
        db_table = "weather"
        ordering = ['date', 'detailTime']
        indexes = [models.Index(fields=['pid'], name='景区pid'),
                   models.Index(fields=['date'], name='Day')]

        app_label = 'ScenceView'




'''上面是创建表总览，下面要具体创建每个景区对应的表---天气，客流量，交通,表名采用 pid+父类名 作为表名'''
