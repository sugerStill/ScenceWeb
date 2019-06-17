from django.db import models


# Create your models here.
class UserHabit(models.Model):
    """
    用户偏好
    """
    pass


class MobileBrandRate(models.Model):
    """
    手机品牌占用率
    """
    brand = models.CharField(max_length=32, verbose_name="品牌")
    pid = models.IntegerField(unique=True, verbose_name="品牌id")
    value = models.FloatField(verbose_name="占有率")

    date = models.DateField(verbose_name="日期")


class MobileTypeRate(models.Model):
    """
    手机机型的占有率

    """
    pid = models.ForeignKey(to="MobileBrandRate", on_delete=models.CASCADE, to_field="pid",
                            verbose_name="品牌标识")
    mobile_type = models.CharField(max_length=32, verbose_name=" 机型")
    value = models.FloatField(verbose_name="占有率")
    date = models.DateField(verbose_name="日期")


class MobileResolutionRate(models.Model):
    """
    手机分辨率占用率
    """
    resolution = models.CharField(max_length=32, verbose_name="分辨率")
    pid = models.IntegerField(verbose_name="id")

    value = models.FloatField(verbose_name="占有率")

    date = models.DateField(verbose_name="日期")


class MobileSystemRate(models.Model):
    """
    手机系统版本占用率
    """
    system = models.CharField(max_length=32, verbose_name=" 系统")

    pid = models.IntegerField(verbose_name="id")
    value = models.FloatField(verbose_name="占有率")

    date = models.DateField(verbose_name="日期")


class MobileOperatorRate(models.Model):
    """
    手机运营商占用率
    """
    operator = models.CharField(max_length=32, verbose_name="运营商")
    pid = models.IntegerField(verbose_name="id")
    value = models.FloatField(verbose_name="占有率")

    date = models.DateField(verbose_name="日期")


class MobileNetworkRate(models.Model):
    """
    手机网络占用率
    """
    network = models.CharField(max_length=32, verbose_name="网络占用率")
    pid = models.IntegerField(verbose_name="id")
    value = models.FloatField(verbose_name="占有率")

    date = models.DateField(verbose_name="日期")


class WetchatPublic(models.Model):
    """公众号信息
    """
    pid = models.IntegerField(unique=True, verbose_name="标识")
    name = models.CharField(max_length=32, verbose_name="公众号名字")
    card = models.CharField(max_length=32, verbose_name="账号")

    averageread = models.IntegerField(verbose_name="平均阅读量")
    hightread = models.IntegerField(verbose_name="最高阅读量")
    averagelike = models.IntegerField(verbose_name="平均点赞")
    hightlike = models.IntegerField(verbose_name="最高点赞")


class WetchatPublicInfo(models.Model):
    """
    公众号的详细数据
    """
    pid = models.ForeignKey(to="WetchatPublic", on_delete=models.CASCADE, to_field="pid")
    keyword = models.CharField(max_length=32, verbose_name="关键词")


class Wetchat_Ariticle(models.Model):
    """
    公众号文章
    """
    pid = models.ForeignKey(to="WetchatPublic", on_delete=models.CASCADE, to_field="pid")

    number = models.IntegerField(verbose_name="文章链接id号")
