import time
import json
from ScenceView.models import JingQuDatabase

'''采用单例模式，同时采用数据内存驻留'''


class GetDataBase(object):
    instance = None
    instance_flag = False
    instance_PassengerFlow = {}  # key是pid，value是data，表示客流量，用来记录用户的浏览记录，同时给短时间内另一用户访问相同内容时直接从内存读取数据，不需要访问数据库
    instance_Traffic = {}  # key是pid，value是data，表示交通拥挤情况
    instance_Weather = {}  # key是pid，value是data，表天气情况

    instance_time = {}  # key是pid，value是time，用来记录用户的访问时间

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            print("new")
        return cls.instance

    def __init__(self):

        if not GetDataBase.instance_flag:
            GetDataBase.instance_flag = True
            print("init")

    # 获取今天客流数据
    @staticmethod
    def peopleflow_information(peoplepid):

        GetDataBase.instance_time[str(peoplepid)] = time.time()  # 记录访问时间
        date = time.strftime("%Y-%m-%d", time.localtime())
        quertset = JingQuDatabase.objects.get(PeoplePid=peoplepid).Flow.filter(date=date).values("num", "detailTime")
        data = []
        timelist = []

        for item in quertset:
            data.append(item['num'])
            timelist.append(item['detailTime'])
        data = json.dumps({"data": data, "time": timelist})
        return data

    # 获取今天交通数据
    @staticmethod
    def trafficindex(pid):

        data = []
        timelist = []
        date = time.strftime("%Y-%m-%d", time.localtime())
        quertset = JingQuDatabase.objects.filter(CityCode=pid)[0].Traffic.filter(date=date).values("TrafficIndex",
                                                                                                   'detailTime')
        for item in quertset:
            data.append(item['TrafficIndex'])
            timelist.append(item['detailTime'])
        data = json.dumps({"data": data, "time": timelist})
        return data

    # 获取以现在时刻-4小时为起点24小时内的天气预报数据
    def getweatherindex(self, pid):
        # 一小时内

        date = time.strftime("%Y-%m-%d", time.localtime())

        quertset = JingQuDatabase.objects.filter(WeatherPid=pid)[0]. \
            weather.filter(date=date). \
            values("date", 'detailTime',
                   'state', 'temperature',
                   'wind')
        result = self.dealwith_data(quertset)
        return json.dumps(result)

    @staticmethod
    def dealwith_data(quertset):
        data = []
        for item in quertset:
            obj = dict()
            obj['date'] = str(item['date'])
            obj['detailTime'] = item['detailTime']
            obj['state'] = item['state']
            obj['wind'] = item['wind']
            obj['temperature'] = item['temperature']
            data.append(obj)
        result = {"weather": data}
        return result

    def getweather_7dindex(self, pid):
        date = time.strftime("%Y-%m-%d", time.localtime())
        quertset = JingQuDatabase.objects.filter(WeatherPid=pid)[0]. \
            weather.filter(date__gte=date). \
            values("date", 'detailTime',
                   'state', 'temperature',
                   'wind')
        result = self.dealwith_data(quertset)
        return json.dumps(result)
