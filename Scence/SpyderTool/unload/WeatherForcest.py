import requests
import re, random, json, importlib, time
from urllib.parse import urlencode
from ScenceView.models import JingQuDatabase

'''获取2k多个城市的历史天气情况'''


class WeatherForcestData(object):
    instance = None
    instance_flag = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
            print("new")
        return cls.instance

    def __init__(self):
        if not WeatherForcestData.instance_flag:
            WeatherForcestData.instance_flag = True
            self.Database = importlib.import_module("Scenic.models")

            self.s = requests.Session()

            self.headers = {
                'Host': 'www.weather.com.cn',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            self.use = ['Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134']

    # 搜索景区天气位置ip

    def getWeatherId(self, name, pid):
        parameter = {
            'cityname': name,

        }
        headers = {
            'Host': 'toy1.weather.com.cn',
            'Referer': 'http: // www.weather.com.cn / weather / 101310201.shtml',

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        href = 'http://toy1.weather.com.cn/search?' + urlencode(parameter)
        response = self.s.get(url=href, headers=headers).text
        ID = re.search("(\d+\w)", response).group(1)
        JingQuDatabase.objects.filter(pid=pid).update(weatherPid=ID)

    # 获取景区天气  ----4小时更新一次
    def getToday(self, lis):
        pid = lis[0]
        weatherpid = lis[1]
        name = lis[2]

        url = 'http://www.weather.com.cn/weather1d/' + weatherpid + '.shtml'
        data = self.s.get(url=url, headers=self.headers)
        par = re.compile('hour3data=(.*)')
        hour3data = re.search(par, data.content.decode("utf-8")).group(1)
        d = re.sub('=', ":", hour3data)
        g = json.loads(d)
        DataName = "PID_" + pid + "_Weather_Data"

        Base = getattr(self.Database, DataName)  # 类
        obj = Base.objects.last()

        # print(obj.data)
        try:
            if obj.data == str(g):  # 与最后一条信息相同则直接不用写入
                print("存在该数据")
                return
        except Exception:
            pass
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        Base(date=date, name=name, data=g).save()
        print("success")
