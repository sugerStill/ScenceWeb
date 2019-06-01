import json
from django.shortcuts import render, HttpResponse
from ScenceView.WebViewTool.City import City
from TrafficView.TrafficTool.TrafficDataBaseOperate import TrafficDatabaseOperate
from TrafficView.models import MainCityTrafficDataBase

'''城市交通模块'''


# 交通首页

def traffic(request):
    return render(request, "Traffic/Traffic_FirstPage.html")


# 城市交通页面
def citytraffic(request, pid):
    name = MainCityTrafficDataBase.objects.get(cityCode=pid).name
    data = City(pid, name)
    return render(request, "Traffic/JiaoTong.html", locals())


# 获取城市交通数据库
def citytraffic_datarequest(reuqest, pid):
    dic = TrafficDatabaseOperate().get_citytraffic_data(pid)
    return HttpResponse(json.dumps(dic))


# 获取道路交通数据
def roadtraffic(request, pid):
    response = TrafficDatabaseOperate().get_roadtraffic_data(pid)
    return HttpResponse(json.dumps(response))


# 获取年度数据
def yeartraffic(request, pid):
    response = TrafficDatabaseOperate().get_yearcitytraffic(pid)
    return HttpResponse(json.dumps(response))
