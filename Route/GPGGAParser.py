from numpy import sum,amax,amin
from folium import Map,PolyLine,Marker,Icon
from dateutil import parser
from datetime import datetime
from gpxpy import geo
import matplotlib.pyplot as plt
import geog

class GPGGAParser:
    def __init__(self,path):
        self.path=path
        self.coordList=list()
        self.heightList=list()
        self.timeList=list()
        self.deltaTimeList=list()
        self.deltaDist=list()
        self.speedList=list()
        self.parser()
        self.__createDeltaTimeList()
        self.__createDeltaDist()
        self.__createSpeedList()
        self.min_height=amin(self.heightList)
        self.max_height=amax(self.heightList)
        self.mean_speed=sum(self.speedList)/len(self.speedList)
        self.min_speed=amin(self.speedList)
        self.max_speed=amax(self.speedList)
        self.distance=sum(self.deltaDist)
        self.flight_time=sum(self.deltaTimeList)*60
        self.routeBuild()
    def parser(self):
        bad_str="0GPGGA,,,,,,0,0,,,M,,M,,*56"
        for line in open(self.path):
            if "GPGGA" in line:
                if bad_str in line:
                    continue
                dataList=line.split(",")[1:]
                dataList[len(dataList)-1]=dataList[len(dataList)-1][:-1]
                coords=self.__latlonParse([dataList[1],dataList[3]])
                self.heightList.append(float(dataList[8]))
                self.timeList.append(parser.parse(dataList[0]))
                self.coordList.append(coords)
    def __latlonParse(self,coords):
        lat=coords[0]
        lon=coords[1]
        lat=float(lat[0:2])+float(lat[2:])/60
        if lon[0]=="0":
            lon=lon[1:]
        lon=float(lon[0:2])+float(lon[2:])/60
        return [lat,lon]
    def getCoordinates(self):
        return self.coordList
    def getMinHeight(self):
        return self.min_height
    def getMaxHeight(self):
        return self.max_height
    def __createDeltaTimeList(self):
        for i in range(len(self.timeList)-1):
            delta=self.timeList[i+1]-self.timeList[i]
            self.deltaTimeList.append(delta.seconds/3600)
    def __createDeltaDist(self):
        lat1,lon1,lat2,lon2=0,0,0,0
        for i in range(len(self.coordList)-1):
            lat1,lon1=self.coordList[i]
            lat2,lon2=self.coordList[i+1]
            delta=geo.haversine_distance(lat1,lon1,lat2,lon2)
            self.deltaDist.append(delta/1000)
    def __createSpeedList(self):
        for i in range(len(self.deltaDist)):
            self.speedList.append(self.deltaDist[i]/self.deltaTimeList[i])
    def getDistance(self):
        return self.distance
    def getMeanSpeed(self):
        return self.mean_speed
    def getMinSpeed(self):
        return self.min_speed
    def getMaxSpeed(self):
        return self.max_speed
    def getFlightTime(self):
        return self.flight_time
    def getDeltaTimeList(self):
        return self.deltaTimeList
    def getSpeedList(self):
        return self.speedList
    def getDistList(self):
        return self.deltaDist
    def getHeightList(self):
        return self.heightList
    def getTimeList(self):
        return self.timeList
    def routeBuild(self):
        map=Map(self.coordList[0],zoom_start=9)
        popup_str="Широта:{0:3f} Долгота:{1:3f}"
        lat1,lon1=self.coordList[0]
        lat2,lon2=self.coordList[len(self.coordList)-1]
        PolyLine(self.coordList,color="red", weight=3, opacity=1).add_to(map)
        Marker([lat1,lon1],popup=popup_str.format(lat1,lon1),icon=Icon(color="blue")).add_to(map)
        Marker([lat2,lon2],popup=popup_str.format(lat2,lon2),icon=Icon(color="green")).add_to(map)
        map.save("map.html")
if __name__=="__main__":
    parser=GPGGAParser("gpgga1.txt")
    time=parser.getTimeList()
    height=parser.getHeightList()
    speed=parser.getSpeedList()
    delta_distance=parser.getDistList()
    distance=list()
    for i in range(len(delta_distance)-1):
        delta=0
        for j in range(i):
            delta+=delta_distance[j]
        distance.append(delta)
    fwd_azimuth=list()
    coordinates=parser.getCoordinates()
    for i in range(len(coordinates)-1):
        fwd=geog.course(coordinates[i],coordinates[i+1])
        fwd_azimuth.append(fwd)
    plt.figure(1)
    delta=len(time)-len(height)
    plt.plot(time,height)
    plt.xlabel("Время(мин)")
    plt.ylabel("Высота(м)")
    plt.figure(2)
    delta=len(time)-len(speed)
    plt.plot(time[:-delta],speed)
    plt.xlabel("Время(мин)")
    plt.ylabel("Скорость(км/ч)")
    plt.figure(3)
    delta=len(time)-len(distance)
    plt.plot(time[:-delta],distance)
    plt.xlabel("Время(мин)")
    plt.ylabel("Дистанция(км)")
    plt.figure(4)
    delta=len(time)-len(fwd_azimuth)
    plt.plot(time[:-delta],fwd_azimuth)
    plt.xlabel("Время(мин)")
    plt.ylabel("Истинный курс(град)")
    plt.show()