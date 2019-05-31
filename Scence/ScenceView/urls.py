# from django.contrib import admin
from django.urls import path
from ScenceView import views

urlpatterns = [

    path("Scence/", views.jingqu, name="jingqu"),
    path("Scence/<int:pid>", views.jingquload, name="Scence"),
    path("getPeopleData/<int:pid>", views.getpeopledata, name="getdata"),

    path("JingQu/Weather/<slug:pid>", views.forcestweather_oneday, name="ForcestWeatherOneDay"),
    path("JingQu/WeatherLong/<slug:pid>", views.forcestweather_longday, name="ForcestWeatherLongDay"),
    path("CityTrafficData/<int:pid>", views.scence_citytraffic, name='getTrafficData'),
    # '''-----------------------------------------------------'''

]
