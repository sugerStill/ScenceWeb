'''城市交通模块'''
from django.shortcuts import render, HttpResponse
import json
from WebView.WebViewTool.City import City
from TrafficView.TrafficTool.TrafficDataBaseOperate import TrafficDatabaseOperate
from TrafficView.models import MainCityTrafficDataBase


# 交通首页

def Traffic(request):
    return render(request, "Traffic/Traffic_FirstPage.html")


# 城市交通页面
def CityTraffic(request, pid):
    name = MainCityTrafficDataBase.objects.filter(cityCode=str(pid)).values('name')[0]['name']
    data = City(pid, name)
    return render(request, "Traffic/JiaoTong.html", locals())


# 获取城市交通数据库
def CityTrafficDataRequest(reuqest, pid):
    dic = TrafficDatabaseOperate().CityTrafficData(['CityCode_', str(pid), '_Traffic'])
    return HttpResponse(json.dumps(dic))


# 获取道路交通数据
def RoadTraffic(request, pid):
    response = TrafficDatabaseOperate().GetRoadTrafficData(['CityCode_', str(pid), '_RoadTraffic'])
    return HttpResponse(json.dumps(response))


# 获取年度数据
def YearTraffic(request, pid):
    response = TrafficDatabaseOperate().GetYearCityTraffic(['CityCode_', str(pid), '_YearTraffic'])
    return HttpResponse(json.dumps(response))
