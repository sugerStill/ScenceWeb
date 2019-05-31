import requests
import json
import time
from urllib.parse import urlencode
from SpyderTool.MulThread import MulitThread
class BaiduTraffic(object):

    def __init__(self, db):
        self.db = db
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        }
        # 获取实时城市交通情况

    def deco(func):
        def Load(self, cityCode):
            data = func(self,cityCode)
            return data
        return Load

    @deco
    def CityTraffic(self, cityCode, timeType='minute'):

        parameter = {
            'cityCode': cityCode,
            'type': timeType  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        try:
            g = json.loads(data.text)
        except Exception as e:
            print("网络链接error:%s" % e)
            return None
        today = time.strftime("%Y-%m-%d", time.localtime())  # 今天的日期
        date = today
        if '00:00' in str(g):
            date = time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24))  # 昨天的日期
        # 含有24小时的数据
        dic = {}
        for item in g['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '13:45'}
            if item["time"] == '00:00':
                date = today
            dic['date'] = date
            dic['index'] = float(item['index'])
            dic['detailTime'] = item['time']
            yield dic
    def  YearTraffic(self, cityCode):

        parameter = {
            'cityCode': cityCode,
            'type': 'day'  # 有分钟也有day
        }
        href = 'https://jiaotong.baidu.com/trafficindex/city/curve?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        obj = json.loads(data.text)

        year = time.strftime("%Y-", time.localtime())  #
        sql = "select   name from MainTrafficInfo where cityCode=" + str(cityCode) + ";"
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print("error:%s" % e)
            self.db.rollback()
            return None
        city = cursor.fetchone()
        for item in obj['data']['list']:
            # {'index': '1.56', 'speed': '32.83', 'time': '04-12'}
            date=year + item['time']
            index=float(item["index"])
            yield {"date": date, "index": index, "city": city}  # {'date': '2019-01-01', 'index': 1.25, 'city': city}
    def RoadData(self,cityCode):


        dic=self.__Roads(cityCode)
        dataList = self.__realTimeRoad(dic,cityCode)
        for item, data in zip(dic['data']['list'], dataList):
            RoadName= item["roadname"]
            Speed=float(item["speed"])
            Direction=item['semantic']
            Bounds = json.dumps({"coords": data['coords']})
            info=json.dumps(data['data'])

            yield {"RoadName": RoadName, "Speed": Speed, "Direction": Direction, "Bounds": Bounds, 'Data': info}



    def __Roads(self, cityCode):
        parameter = {
            'cityCode': cityCode,
            'roadtype': 0
        }
        href = ' https://jiaotong.baidu.com/trafficindex/city/roadrank?' + urlencode(parameter)
        data = self.s.get(url=href, headers=self.headers)
        dic = json.loads(data.text)
        return dic


    def __realTimeRoad(self, dic, cityCode):


        for item, i in zip(dic['data']['list'], range(1, 11)):
            # {'id': '7454364524', 'time': '201904141410', 'citycode': '134', 'district_type': '0', 'roadsegid': '福昆线-4', 'speed': '28.86', 'yongdu_length': '0.75', 'road_type': '3', 'roadname': '福昆线', 'index': '1.89', 'index_level': 2, 'length': '5.76', 'semantic': '从湖盘桥到顺济桥，西向北', 'links': '15776017580|15900320950|15226870110|15226963550|15227678580|15226326330|15227590310|15226047270|15225774350|15228067920|15227792960|15226046560|15894756130|15889255860|15228617410|16050317430|16050307670|15890367700|15776003900|15776003890|15899025410|15226671450|15226778680|15227244090|15715805110|15892968130|15226870440|15889322250|15641506000|15520527690|16055714390|15875249260|15225863470|15227678730|15228155660|15226047240|16055689940|16055682910|15554585850|16055680120|16055678110|15226869660|15227676810|15227589890|15227588810|16176834310|16176951060|15890883470|15227243760|15227442230|15641509421', 'location': '118.555224,24.877892', 'nameadd': ''}

            data=self.__RealTimeRoadData(item['roadsegid'], i,cityCode)
            yield  data


    #道路请求
    def __RealTimeRoadData(self,pid, i,cityCode):
        parameter = {
            'cityCode': cityCode,
            'id': pid
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
        return {"data": realData, "coords": bounds}
