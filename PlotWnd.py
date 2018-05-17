import sys
import geog
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

class PlotWnd(QtWidgets.QWidget):
    def __init__(self,time,speed,height,dist,coord):
        QtWidgets.QWidget.__init__(self,parent=None)
        self.resize(150,200)
        self.time=time
        self.delta_distance=dist
        self.height=height
        self.speed=speed
        self.coordinates=coord
        self.distance=list()
        self.fwd_azimuth=list()
        self.mainLayer=QtWidgets.QVBoxLayout()
        self.distButton=QtWidgets.QPushButton("Дистанция",self)
        self.speedButton=QtWidgets.QPushButton("Скорость",self)
        self.heightButton=QtWidgets.QPushButton("Высота",self)
        self.azimuthButton=QtWidgets.QPushButton("Истинный курс",self)
        self.mainLayer.addWidget(self.distButton)
        self.mainLayer.addWidget(self.speedButton)
        self.mainLayer.addWidget(self.heightButton)
        self.mainLayer.addWidget(self.azimuthButton)
        self.distButton.clicked.connect(self.plotDistance)
        self.speedButton.clicked.connect(self.plotSpeed)
        self.heightButton.clicked.connect(self.plotHeight)
        self.azimuthButton.clicked.connect(self.plotFwdAzimuth)
        self.initUI()
    def initUI(self):
        self.setLayout(self.mainLayer)
        self.setWindowTitle("Визуализация данных")
        self.show()
    @pyqtSlot()
    def plotDistance(self):
        if len(self.distance)==0:
            for i in range(len(self.delta_distance)-1):
                delta=0
                for j in range(i):
                    delta+=self.delta_distance[j]
                self.distance.append(delta)
        delta=len(self.time)-len(self.distance)
        plt.plot(self.time[:-delta],self.distance)
        plt.xlabel("Время(мин)")
        plt.ylabel("Дистанция(км)")
        plt.title("Дистанция")
        plt.show()
    @pyqtSlot()
    def plotSpeed(self):
        delta=len(self.time)-len(self.speed)
        plt.plot(self.time[:-delta],self.speed)
        plt.xlabel("Время(мин)")
        plt.ylabel("Скорость(км/ч)")
        plt.title("Скорость")
        plt.show()
    @pyqtSlot()
    def plotHeight(self):
        delta=len(self.time)-len(self.height)
        plt.plot(self.time,self.height)
        plt.xlabel("Время(мин)")
        plt.ylabel("Высота(м)")
        plt.title("Высота")
        plt.show()
    @pyqtSlot()
    def plotFwdAzimuth(self):
        if len(self.fwd_azimuth)==0:
            for i in range(len(self.coordinates)-1):
                fwd=geog.course(self.coordinates[i],self.coordinates[i+1])
                self.fwd_azimuth.append(fwd)
        delta=len(self.time)-len(self.fwd_azimuth)
        plt.plot(self.time[:-delta],self.fwd_azimuth)
        plt.xlabel("Время(мин)")
        plt.ylabel("Истинный курс(град)")
        plt.title("Истинный курс")
        plt.show()
if __name__ == "__main__":
    from GPGGAParser import *
    parser=GPGGAParser("gpgga1.txt")
    time=parser.getTimeList()
    dist=parser.getDistList()
    speed=parser.getSpeedList()
    height=parser.getHeightList()
    coord=parser.getCoordinates()
    app = QtWidgets.QApplication(sys.argv)
    wnd = PlotWnd(time,speed,height,dist,coord)
    sys.exit(app.exec_())