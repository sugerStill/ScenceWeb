from django.contrib import admin
from django.urls import path
from ScenceView import views

urlpatterns = [

    path("Scence/", views.JingQu, name="jingqu"),
    path("Scence/<int:pid>", views.JingQuLoad, name="Scence"),
    path("getPeopleData/<int:pid>", views.getPeopleData, name="getdata"),

    path("JingQu/Weather/<slug:pid>", views.ForcestWeatherOneDay, name="ForcestWeatherOneDay"),
    path("JingQu/WeatherLong/<slug:pid>", views.ForcestWeatherLongDay, name="ForcestWeatherLongDay"),
    path("CityTrafficData/<int:pid>", views.ScienceCityTraffic, name='getTrafficData'),
    # '''-----------------------------------------------------'''

]
