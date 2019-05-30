
from abc import  ABC,abstractmethod


class Traffic(ABC):



    @abstractmethod
    def CityTraffic(self, cityCode):
        pass


    #道路数据获取
    @abstractmethod

    def RoadData(self,cityCode):
        pass

    @abstractmethod
    def YearTraffic(self,cityCode,year):
        pass

    # def Roads(self, cityCode):
    #
    #     pass
    #
    # # 某条路实时路况
    # @abstractmethod
    #
    # def __realTimeRoad(self, dic, cityCode):
    #     pass
    # @abstractmethod
    #
    # def __RealTimeRoadData(self, RoadUrl, i):
    #     pass
