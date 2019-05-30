import requests, json, time, datetime, calendar

from urllib.parse import quote, urlencode
from concurrent import futures

'''获取位置流量趋势'''


class PlaceTraffic(object):
    instance = None
    instance_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not PlaceTraffic.instance_flag:
            PlaceTraffic.instance_flag = True
            self.headers = {
                'Host': 'heat.qq.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

            }
            self.s = requests.Session()
            # 时间段最长15天，最小时间间隔是1分钟range，开始时间最早2016-07-18
            self.date_begin = "2016-12-27"
            self.date_end = "2017-01-02"  # 一般设为预测天
            self.range = 1

    def getAllProvince(self):
        href = "https://heat.qq.com/api/getAllProvince.php?sub_domain="
        d = self.s.get(url=href, headers=self.headers)
        g = json.loads(d.text)
        l = []
        # [l.append(item["province"]) for item in g]

        [self.getAllCity(item["province"]) for item in g]

    def getAllCity(self, province):
        # 这里不需要quote中文转url，因为后面的urlencode自动会转
        parameter = {
            "province": province,
            "sub_domain": ''
        }
        href = "https://heat.qq.com/api/getCitysByProvince.php?" + urlencode(parameter)
        d = self.s.get(url=href, headers=self.headers)
        g = json.loads(d.text)
        l = []
        # [l.append(item["city"]) for item in g]
        futures.ThreadPoolExecutor(45).map(self.getRegionsByCity, [[province, item["city"]] for item in g])

    def getRegionsByCity(self, lis):
        parameter = {
            'province': lis[0],
            'city': lis[1],
            'sub_domain': ''
        }
        href = "https://heat.qq.com/api/getRegionsByCity.php?" + urlencode(parameter)
        d = self.s.get(url=href, headers=self.headers)
        g = json.loads(d.text)
        # l = []
        # t = []
        # [l.append(item["id"] ) for item in g]
        # [t.append(item["name"]) for item in g]
        [self.getLocations(item['name'], item["id"]) for item in g]

    # range表示数据间隔，最小1
    def getLocations(self, region_name, id):
        parameter = {
            'region': id,
            'date_begin': self.date_begin,
            'date_end': self.date_end,
            'range': self.range,
            'predict': False  # 是否获取预测数据,若为true，预测那天的键需要加上「预测」两字
        }

        href = "https://heat.qq.com/api/getLocation_uv_percent_new.php?" + urlencode(parameter)
        d = self.s.get(url=href, headers=self.headers)
        g = json.loads(d.text)
        start = time.strptime(self.date_begin, "%Y-%m-%d")
        end = time.strptime(self.date_end, "%Y-%m-%d")
        interval = 0  # 间隔天数

        # 获取间隔日期 ----仅限于最大周期15天
        l = []  # 保存日期---作为键来获取数据
        if not end.tm_year - start.tm_year:  # 同一年
            interval = end.tm_yday - start.tm_yday
            startday = start.tm_mday
            if not end.tm_mon - start.tm_mon:  # 同一月
                [l.append(i.isoformat()) for i in
                 [datetime.date(start.tm_year, start.tm_mon, startday + i) for i in range(0, interval)]]
            else:
                d = calendar.monthrange(start.tm_year, start.tm_mon)[1]  # 本月日数
                critical = d - start.tm_mday  # 本月剩下几天
                l1 = [datetime.date(start.tm_year, start.tm_mon, startday + i) for i in range(0, interval + 1) if
                      i <= critical]
                l2 = [
                    datetime.date(start.tm_year, end.tm_mon, i) for i in range(1, interval - critical)]
                l1.extend(l2)
                [l.append(i.isoformat()) for i in l1]

        else:  # 跨年
            interval = end.tm_mday + 31 - start.tm_mday
            startday = start.tm_mday
            critical = 31 - start.tm_mday  # 本月剩下几天
            l1 = [datetime.date(start.tm_year, start.tm_mon, startday + i) for i in range(0, interval + 1) if
                  i <= critical]
            l2 = [
                datetime.date(end.tm_year, end.tm_mon, i) for i in range(1, interval - critical)]
            l1.extend(l2)
            [l.append(i.isoformat()) for i in l1]
        data = [g[key] for key in l]
        print("1")


p = PlaceTraffic()
p.getAllProvince()
