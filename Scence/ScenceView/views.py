from django.shortcuts import render, HttpResponse, Http404
import json, pickle
from ScenceView.WebViewTool.GetJingQUData import Information
from ScenceView.WebViewTool.DataBaseOperation import GetDataBase
from ScenceView.models import JingQuDatabase

'''景区模块'''


# 景区页面
def JingQu(request):
    return render(request, "JingQu/JingQu_FirstPage.html")


# 景区
def JingQuLoad(request, pid):

    try:
        data = JingQuDatabase.objects.filter(PeoplePid=pid).values("name", "CityCode",'WeatherPid')[0]
    except Exception as e:
        raise Http404
    name = data["name"]
    cityCode = data["CityCode"]
    WeatherPid=data['WeatherPid']
    information = Information(pid, name, cityCode,WeatherPid)
    data = information.getInformation()

    url = "JingQu/" + str(pid) + ".html"
    return render(request, url, locals())


# 获取实时客流数据
def getPeopleData(request, pid):
    data = GetDataBase().PeopleFlowInformation(pid)

    return HttpResponse(data)


# 景区城市交通状态
def ScienceCityTraffic(request, pid):
    print(pid)
    dic = GetDataBase().TrafficIndex(str(pid))
    return HttpResponse(dic)


# 获取景区天气预报
def ForcestWeatherOneDay(request, pid):
    data = GetDataBase().getWeatherIndex(pid)
    return HttpResponse(data)


def ForcestWeatherLongDay(request, pid):
    data = GetDataBase().getWeather7dIndex(pid)
    return HttpResponse(data)
