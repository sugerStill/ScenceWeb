import requests
import json
from SpyderTool.MulThread import MulitThread
import time
import re
from urllib.parse import urlencode

'''下面是针对高德的程序'''


class GaodeTraffic(object):
    instance = None
    instance_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            print("new")
        return cls.instance

    def __init__(self):
        if not GaodeTraffic.instance_flag:
            GaodeTraffic.instance_flag = True
            self.s = requests.Session()
            self.headers = {
                'Host': 'report.amap.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

            }

    # 获取实时城市交通情况
    def getCityTraffic(self, lis):
        DatabaseList = lis[0]

        self.cityCode = lis[1]
        url = "http://report.amap.com/ajax/cityHourly.do?cityCode=" + str(self.cityCode)
        data = self.s.get(url=url, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception:
            return False
        DataName = ''.join(DatabaseList)
        Base = getattr(self.Database, DataName)  # 类
        date = time.strftime("%Y-%m-%d", time.localtime())
        print(DataName)
        for item in g:
            base = Base()
            base.date = date
            base.time = time.strftime("%H:%M", time.localtime(int(item[0]) / 1000 + 3600 * 8))
            base.data = float(item[1])
            base.save()
        print("ok")
        return True

    # 获取城区前10拥挤道路信息

    def getRoad(self, lis):
        DatabaseList = lis[0]
        cityCode = lis[1]
        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": cityCode
        }
        url = "https://report.amap.com/ajax/roadRank.do?" + urlencode(req)
        data = self.s.get(url=url, headers=self.headers)
        date = time.strftime("%Y-%m-%d", time.localtime())
        DetailTime = time.strftime("%H:%M", time.localtime())

        DataName = ''.join(DatabaseList)
        Base = getattr(self.Database, DataName)  # 类
        try:
            Route = json.loads(data.text)  # 道路经纬度
        except Exception:
            return
        listId = []  # 记录道路pid
        listRoadName = []  # 记录道路名
        listDir = []  # 记录道路方向
        listSpeed = []  # 记录速度
        for item in Route["tableData"]:
            listRoadName.append(item["name"])  # 道路名
            listDir.append(item["dir"])  # 方向
            listSpeed.append(item["speed"])  # 速度
            listId.append(item["id"])  # 道路pid
        dic = {}
        dic["route"] = Route
        dic["listId"] = listId
        dic["listRoadName"] = listRoadName
        dic["listDir"] = listDir
        dic["listSpeed"] = listSpeed
        dataList = self.realTimeRoad(dic, cityCode)

        for item, data in zip(Route["tableData"], dataList['data']):
            b = Base()
            b.date = date
            b.DetailTime = DetailTime
            b.name = item["name"]
            b.speed = float(item["speed"])
            b.data = json.dumps(data)
            b.direction = item['dir']
            b.bounds = json.dumps({"coords": item['coords']})
            b.save()

    # 某条路实时路况
    def realTimeRoad(self, dic, cityCode):
        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": cityCode,
            'lineCode': ''

        }
        url = "https://report.amap.com/ajax/roadDetail.do?" + urlencode(req)
        threadlist = []
        data = []
        for id, i in zip(dic["listId"],
                         range(0, (dic["listId"]).__len__())):
            RoadUrl = url + str(id)
            t = MulitThread(target=self.RealTimeRoadData, args=(RoadUrl, i,))  # i表示排名
            time.sleep(1)
            t.start()
            threadlist.append(t)
        for t in threadlist:
            t.join()
            if t.get_result is not None:
                data.append(t.get_result)

        ##排好序列
        if len(data) > 0:
            sorted(data, key=lambda x: ["num"])

        return {"data": data, "info": dic}

    def RealTimeRoadData(self, RoadUrl, i):
        data = self.s.get(url=RoadUrl, headers=self.headers)
        try:
            g = json.loads(data.text)  # 拥堵指数
        except Exception:
            return None
        l = []  # 拥堵指数
        t = []  # 时间
        for item in g:
            t.append(time.strftime("%H:%M", time.strptime(time.ctime(int(item[0] / 1000 + 3600 * 8)))))
            l.append(item[1])
        # {排名，时间，交通数据}
        realData = {"num": i, "time": t, "data": l}
        return realData

    # 城市年交通状态
    def YearTraffic(self, lis):
        DatabaseList = lis[0]
        city = lis[1]
        yearpid = lis[2]
        url = "http://report.amap.com/ajax/cityDailyQuarterly.do?"

        DataName = ''.join(DatabaseList)
        Base = getattr(self.Database, DataName)  # 类
        # year键表示哪一年 的数据
        req = {
            "cityCode": yearpid,
            "year": 2019,  # 年份
            "quarter": ''  # 第几季
        }

        for i in range(1, 3):
            req["quarter"] = 1
            url = url + urlencode(req)
            data = self.s.get(url=url, headers=self.headers)
            g = eval(data.text)
            for date, index in zip(g["categories"], g['serieData']):
                b = Base()
                b.date = date
                b.index = index
                b.city = city
                b.save()

    # 获取城区经纬度
    def getLngLat(self, name):
        req = {
            "roadType": 0,
            "timeType": 0,
            "cityCode": self.cityCode
        }
        url = "https://report.amap.com/ajax/roadRank.do?" + urlencode(req)
        data = self.s.get(url=url, headers=self.headers)
        Route = json.loads(data.text)  # 路径
        route = Route['tableData'][0]['coords'][0]

        lat = route['lat']
        lon = route['lon']
        l = []
        l.append(name)
        l.append(self.cityCode)
        l.append(lon)
        l.append(lat)


class BaiduTraffic(object):
    instance = None
    instance_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):

        if not BaiduTraffic.instance_flag:
            BaiduTraffic.instance_flag = True
            self.s = requests.Session()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

            }

    '''数据类型city_coords: "11555387.73,2918272.23"
    citycode: "249"
    cityname: "曲靖"
    index: "1.14"
    index_level: 1
    last_index: "1.28"
    provincecode: 28
    provincename: "云南"
    speed: "34.91"
    time: "201904141315"
    weekRate: -0.109'''

    # 获取城市的信息-获取所有交通数据
    def getCity(self):
        href = 'https://jiaotong.baidu.com/trafficindex/city/list?callback=jsonp_1555219401678_9836662'
        d = self.s.get(url=href, headers=self.headers)
        data = re.search(re.compile("\((.*?)\)"), d.text).group(1)
        obj = json.loads(data)

        for item in obj['data']['list']:
            l = []
            l.append(item['city_coords'])  # 地理位置
            l.append(item['citycode'])  # 城市pid
            l.append(item['cityname'])  # 城市名
            l.append(item['provincecode'])  # 省份pid
            l.append(item['provincename'])  # 省份名

            # store.append(item['cityname'])
            # self.trafficindex(item['citycode'])  # 开始爬取该城市当他天24小时内的信息

            # self.getRoad(item['citycode'])

    # 开始爬取该城市当他天24小时内的信息---以现在时刻为终点24小时内的数据
    def getCityTraffic(self, lis, timeType='minute'):
        DatabaseList = lis[0]
        self.cityCode = lis[1]
        parameter = {
            'cityCode': self.cityCode,
            'type': timeType  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)

        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)
        DataName = ''.join(DatabaseList)  # 生成数据库名"

        Base = getattr(self.Database, DataName)  # 获取数据库类

        date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        # 含有24小时的数据
        for item in obj['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '13:45'}
            base = Base()
            if item["time"] == '00:00':
                date = today
            base.date = date
            base.time = item['time']

            base.data = float(item["index"])
            base.save()
        return True

    # 近7天数据

    def getWeekCityTraffic(self, lis):
        DatabaseList = lis[0]
        city = lis[1]
        cityCode = DatabaseList[1]
        parameter = {
            'cityCode': cityCode,
            'type': 'day'  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)
        DataName = ''.join(DatabaseList)  # 生成数据库名"
        Base = getattr(self.Database, DataName)  # 获取数据库类

        year = time.strftime("%Y-", time.localtime())  #

        for item in obj['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '04-12'}
            base = Base()
            base.date = year + item['time']
            base.city = city
            base.index = float(item["index"])
            base.save()
        return True

    '''citycode: "303"
district_type: "0"
id: "7454323617"
index: "2.75"
index_level: 3
length: "2.32"
links: "15267952040|16128426680|16128402330|15264436340|15262336630|15274674160|15265536340|15271980050|15273996920|15261891040|15267950950|15658428900|15658435150|15274672230|15678364820|15678360740|15267952330|15528967260|15748756090|15875108930|15266991950|15695158740|15695157220|15695158630|15266091260|15265702000|15261176380|15274634140|15267514250"
location: "116.728768,23.392184"
nameadd: ""
road_type: "3"
roadname: "福昆线"
roadsegid: "福昆线-97"
semantic: "从原外马路新华交行到天山南路，北向南"
speed: "13.53"
time: "201904141400"
yongdu_length: "0.75"'''

    # 获取十条道路的信息
    def getRoad(self, lis):
        DatabaseList = lis[0]
        cityCode = lis[1]
        parameter = {
            'cityCode': cityCode,
            'roadtype': 0
        }
        href = ' https://jiaotong.baidu.com/trafficindex/city/roadrank?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)
        dataList = []

        for item, i in zip(obj['data']['list'], range(1, 11)):
            # {'id': '7454364524', 'time': '201904141410', 'citycode': '134', 'district_type': '0', 'roadsegid': '福昆线-4', 'speed': '28.86', 'yongdu_length': '0.75', 'road_type': '3', 'roadname': '福昆线', 'index': '1.89', 'index_level': 2, 'length': '5.76', 'semantic': '从湖盘桥到顺济桥，西向北', 'links': '15776017580|15900320950|15226870110|15226963550|15227678580|15226326330|15227590310|15226047270|15225774350|15228067920|15227792960|15226046560|15894756130|15889255860|15228617410|16050317430|16050307670|15890367700|15776003900|15776003890|15899025410|15226671450|15226778680|15227244090|15715805110|15892968130|15226870440|15889322250|15641506000|15520527690|16055714390|15875249260|15225863470|15227678730|15228155660|15226047240|16055689940|16055682910|15554585850|16055680120|16055678110|15226869660|15227676810|15227589890|15227588810|16176834310|16176951060|15890883470|15227243760|15227442230|15641509421', 'location': '118.555224,24.877892', 'nameadd': ''}

            dataList.append(self.roadcurve(item['roadsegid'], i, cityCode))
        DataName = ''.join(DatabaseList)
        Base = getattr(self.Database, DataName)  # 类
        date = time.strftime("%Y-%m-%d", time.localtime())
        DetailTime = time.strftime("%H:%M", time.localtime())
        for item, data in zip(obj['data']['list'], dataList):
            b = Base()
            b.date = date
            b.DetailTime = DetailTime
            b.name = item["roadname"]
            b.speed = float(item["speed"])
            b.data = json.dumps(data['data'])
            b.direction = item['semantic']
            b.bounds = json.dumps({"coords": data['info']})
            b.save()

    def roadcurve(self, id, i, cityCode):
        parameter = {
            'cityCode': cityCode,
            'id': id
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/roadcurve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)
        # {'id': '5553895109', 'datatime': '14:55', 'roadsegid': '温陵北路-12', 'speed': '15.99', 'congestLength': '0.57', 'congestIndex': '2.51', 'citycode': '134'}
        t = []
        l = []
        for item in obj['data']['curve']:  # 交通数据
            t.append(item['datatime'])
            l.append(item['congestIndex'])
        realData = {"num": i, "time": t, "data": l}
        bounds = []
        for item in obj['data']['location']:  # 卫星数据
            bound = {}
            for locations, count in zip(item.split(","), range(0, item.split(",").__len__())):
                if count % 2 != 0:

                    bound['lat'] = locations
                else:
                    bound['lon'] = locations
            bounds.append(bound)
        return {"data": realData, "info": bounds}
