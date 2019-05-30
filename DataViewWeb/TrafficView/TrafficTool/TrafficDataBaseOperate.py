import importlib, json


class TrafficDatabaseOperate(object):
    def __init__(self):
        self.Database = importlib.import_module("Scenic.models")

    ###-日常数据库操作#####
    # 获取日常数据
    def CityTrafficData(self, DatabaseList):

        DataName = ''.join(DatabaseList)  # 生成数据库名"
        Base = getattr(self.Database, DataName)  # 获取数据库类
        ct = Base.objects.all().values("data", "time").iterator()
        Time = []
        data = []
        for item in ct:
            Time.append(item['time'])
            data.append(item['data'])
        dic = {"Citytraffic": {"data": data, "time": Time}}
        return dic

    # 获取道路日常数据
    def GetRoadTrafficData(self, DatabaseList):
        dic = {}
        route = []

        listRoadName = []
        listSpeed = []
        data = []
        directions = []
        DataName = ''.join(DatabaseList)  # 生成数据库名"
        Base = getattr(self.Database, DataName)  # 获取数据库类
        cd = Base.objects.all().values("name", "data", "bounds", "speed", 'direction').iterator()
        for item in cd:
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
    def GetYearCityTraffic(self, DatabaseList):
        categories = []
        serieData = []

        DataName = ''.join(DatabaseList)
        Base = getattr(self.Database, DataName)  # 类
        all = Base.objects.all().values("date", "index")
        for item in all:
            categories.append(item['index'])
            serieData.append(str(item['date']))
        return {"data": categories, "time": serieData}
