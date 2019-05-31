from SpyderTool.Function.ScenceFunction import ScenceFunction

from SpyderTool.Function.TrafficFunction import TraffciFunction


def initscencedatabase():
    d = ScenceFunction()
    d.initdatabase()


def inittrafficdatabase():
    t = TraffciFunction()
    t.initdatabase()


'''初始化数据库'''
if __name__ == "__main__":
    print("请输入操作选项：1.初始化景区数据库  2.初始化交通数据库")
    state = input()
    if state == 1:
        initscencedatabase()
    if state == 2:
        inittrafficdatabase()
    else:
        print("输入有误！")
