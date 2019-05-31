from django.urls import path
from TrafficView import views

urlpatterns = [

    # 交通首页
    path("Traffic/", views.traffic, name="traffic"),
    # 城市交通页面
    path("Traffic/<int:pid>", views.citytraffic, name="cityTraffic"),
    # 录入数据库
    # 读取道路数据库
    # 更新城市交通数据库
    path('YearTrafficData/<int:pid>', views.yeartraffic, name="getYearTraffic"),

    # 请求道路交通数据库
    path("RequestRoadTrafficData/<int:pid>", views.roadtraffic, name="getRoadTraffic"),
    # 请求城市交通数据库
    path("CityTrafficDataRequest/<int:pid>", views.citytraffic_datarequest, name='requestCityTrafficData'),

]
