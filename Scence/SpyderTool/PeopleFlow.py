import pymysql, json, requests, re, time
from urllib.parse import urlencode


class ScencePeopleFlow:
    def __init__(self, PeoplePid, db):
        self.db = db
        self.PeoplePid = PeoplePid
        self.s = requests.Session()
        self.headers = {
            'Host': 'jiaotong.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'
        }

    # 获取今天到目前为止所有客流数据
    def deco(func):
        def Load(self, PeopleTablePid, date, num, detailTime):
            data = func(self, PeopleTablePid, date, num, detailTime)
            return data

        return Load

    @property
    def PeopleFlowInfo(self):

        # type键 1 表示今天 2 表示昨天 3表示最近的节日
        pre_url = 'http://jiaotong.baidu.com/trafficindex/dashboard/curve?'
        u = {
            'type': '1',
            "area_type": "1",
            'area_id': str(self.PeoplePid)
        }
        url = pre_url + urlencode(u)
        data = self.s.get(url=url, headers=self.headers)
        try:
            g = json.loads(data.content)
        except Exception:
            p = re.compile("\((.*?)\)", re.S)
            data = re.search(p, data.text)
            g = json.loads(data.group(1))

        for item in g["data"]['list']:
            detailTime = item["data_time"].split(" ")[1]
            num = int(item['count'])
            yield detailTime, num

    @deco
    def LoadDatabase(self, pid, date, num, detailTime):
        cursor = self.db.cursor()

        sql = "insert into peopleFlow(pid_id,date,num,detailTime) values ('%d','%s','%d','%s');" % (
            pid, date, num, detailTime)
        try:
            cursor.execute(sql)
            self.db.commit()

        except Exception as e:
            print(e)
            self.db.rollback()
            return None
        cursor.close()
