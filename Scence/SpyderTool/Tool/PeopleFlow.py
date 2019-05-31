import json
import requests
import re
from urllib.parse import urlencode


class ScencePeopleFlow:
    def __init__(self, peoplepid, db):
        self.db = db
        self.peoplepid = peoplepid
        self.s = requests.Session()
        self.headers = {
            'Host': 'jiaotong.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
        }

    @property
    def peopleflow_info(self):

        # type键 1 表示今天 2 表示昨天 3表示最近的节日
        pre_url = 'http://jiaotong.baidu.com/trafficindex/dashboard/curve?'
        u = {
            'type': '1',
            "area_type": "1",
            'area_id': str(self.peoplepid)
        }
        url = pre_url + urlencode(u)
        data = self.s.get(url=url, headers=self.headers)
        try:
            g = json.loads(data.content)
        except Exception as e:
            print("%s: 切换正则匹配格式" % e)
            p = re.compile('''\((.*?)\)''', re.S)
            data = re.search(p, data.text)
            g = json.loads(data.group(1))

        for item in g["data"]['list']:
            detailtime = item["data_time"].split(" ")[1]
            num = int(item['count'])
            yield detailtime, num
