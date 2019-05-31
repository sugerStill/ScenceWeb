from django.shortcuts import render, HttpResponse, Http404
from ScenceView.WebViewTool.GetJingQUData import Information
from ScenceView.WebViewTool.DataBaseOperation import GetDataBase
from ScenceView.models import JingQuDatabase

'''景区模块'''


# 景区页面
def jingqu(request):
    return render(request, "JingQu/JingQu_FirstPage.html")


# 景区
def jingquload(request, pid):
    try:
        data = JingQuDatabase.objects.filter(PeoplePid=pid).values("name", "CityCode", 'WeatherPid')[0]
    except Exception as e:
        raise Http404
    name = data["name"]
    citycode = data["CityCode"]
    weatherpid = data['WeatherPid']
    information = Information(pid, name, citycode, weatherpid)
    data = information.getinformation()

    url = "JingQu/" + str(pid) + ".html"
    return render(request, url, locals())


# 获取实时客流数据
def getpeopledata(request, pid):
    data = GetDataBase().peopleflow_information(pid)

    return HttpResponse(data)


# 景区城市交通状态
def scence_citytraffic(request, pid):
    dic = GetDataBase().trafficindex(str(pid))
    return HttpResponse(dic)


# 获取景区天气预报
def forcestweather_oneday(request, pid):
    data = GetDataBase().getweatherindex(pid)
    return HttpResponse(data)


def forcestweather_longday(request, pid):
    data = GetDataBase().getweather_7dindex(pid)
    return HttpResponse(data)
