import importlib
import json
import time

from TrafficView.models import MainCityTrafficDataBase


class TrafficDatabaseOperate(object):
    def __init__(self):
        pass

    ###-日常数据库操作#####
    # 获取日常数据
    def get_citytraffic_data(self, citycode):
        date = time.strftime("%Y-%m-%d", time.localtime())
        timelist = []
        data = []
        result = MainCityTrafficDataBase.objects.get(cityCode=citycode). \
            CityTraffic.filter(date=date).values("detailtime", 'trafficindex'). \
            iterator()
        for item in result:
            timelist.append(item['detailtime'])
            data.append(item['trafficindex'])
        dic = {"Citytraffic": {"data": data, "time": timelist}}
        return dic

    # 获取道路日常数据
    def get_roadtraffic_data(self, citycode):
        date = time.strftime("%Y-%m-%d", time.localtime())

        dic = {}
        route = []

        listRoadName = []
        listSpeed = []
        data = []
        directions = []
        result = MainCityTrafficDataBase.objects.get(cityCode=citycode). \
            RoadTraffic.filter(date=date, flag=True). \
            values("name", "data", "bounds", "speed", 'direction'). \
            iterator()
        for item in result:
            route.append({"coords": json.loads(item['bounds'])['coords']})
            listRoadName.append(item['name'])
            listSpeed.append(item['speed'])
            data.append(json.loads(item['data']))
            directions.append(item['direction'])

        dic["route"] = {"tableData": route}
        dic["listRoadName"] = listRoadName
        dic["listSpeed"] = listSpeed
        dic['dir'] = directions
        response = {}
        response['roadData'] = {"data": data, "info": dic}
        return response

    # 获取季度交通数据
    def get_yearcitytraffic(self, citycode):
        categories = []
        serieData = []

        all = MainCityTrafficDataBase.objects.get(cityCode=citycode). \
            YearTraffic.filter().values("date", "trafficindex") \
            .iterator()
        for item in all:
            categories.append(item['trafficindex'])
            serieData.append(str(item['date']))
        data = {"data": categories, "time": serieData}
        print(data)
        return data
