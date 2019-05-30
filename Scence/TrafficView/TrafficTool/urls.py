from django.contrib import admin
from django.urls import path
from ScenceView import views

urlpatterns = [

    # 交通首页
    path("Traffic/", views.Traffic, name="traffic"),
    # 城市交通页面
    path("Traffic/<int:pid>", views.CityTraffic, name="cityTraffic"),
    # 录入数据库
    # 读取道路数据库
    # 更新城市交通数据库
    path('YearTrafficData/<int:pid>', views.YearTraffic, name="getYearTraffic"),

    # 请求道路交通数据库
    path("RequestRoadTrafficData/<int:pid>", views.RoadTraffic, name="getRoadTraffic"),
    # 请求城市交通数据库
    path("CityTrafficDataRequest/<int:pid>", views.CityTrafficDataRequest, name='requestCityTrafficData'),

]
