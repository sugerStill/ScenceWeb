from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=32, verbose_name="省份")  # 省份
    provincepid = models.IntegerField(unique=True, verbose_name="省份唯一标识")  # 省份id

    class Meta:
        app_label = "weather"
        db_table = "province"


class City(models.Model):
    pid = models.ForeignKey(to="Province", on_delete=models.CASCADE, to_field="provincepid", related_name="Pid")
    name = models.CharField(max_length=32, verbose_name="城市名")
    citypid = models.IntegerField(unique=True, verbose_name="城市唯一标识")  # 城市id

    class Meta:
        app_label = "weather"

        db_table = "city"


class WeatherManager(models.Model):
    pid = models.ForeignKey(to="City", on_delete=models.CASCADE, to_field="citypid", related_name="WeatherManager")
    historypid = models.IntegerField(unique=True, verbose_name="历史天气id")

    class Meta:
        app_label = "weather"
        db_table = "weathermanager"


class HistoryWeather(models.Model):
    pid = models.ForeignKey(to="WeatherManager", on_delete=models.CASCADE, to_field="historypid",
                            related_name="History")
    date = models.DateField(verbose_name="日期")
    state = models.TextField(verbose_name="天气状况")
    temperature = models.TextField(verbose_name="气温")
    wind = models.TextField(verbose_name='风力风向')

    class Meta:
        app_label = "weather"
        db_table = "history"
