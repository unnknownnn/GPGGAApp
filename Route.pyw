import sys
from os import getcwd
from GPGGAParser import *
from PlotWnd import *
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtCore import Qt,QUrl,pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebKitWidgets import QWebView

class MainWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent=None)
        self.file_path=self.__getPath()
        self.setFixedSize(1000,600)
        self.parser=GPGGAParser("gpgga1.txt")
        self.mapVLayout=QtWidgets.QVBoxLayout()
        self.mapGridLayout=QtWidgets.QGridLayout()
        self.updateButton=QtWidgets.QPushButton("Обновить карту",self)
        self.changeRoute=QtWidgets.QPushButton("Изменить маршрут",self)
        self.routeData=QtWidgets.QPushButton("Данные по маршруту",self)
        self.zoomButton=QtWidgets.QPushButton("Увеличить",self)
        self.advancedButton=QtWidgets.QPushButton("Дополнительно",self)
        self.plotButton=QtWidgets.QPushButton("Визуализация данных",self)
        self.webMap=QWebView(self)
        self.url=QUrl("file:///"+self.file_path +"/map.html")
        self.webMap.load(self.url)
        self.mapVLayout.addWidget(self.webMap)
        self.mapVLayout.addLayout(self.mapGridLayout)
        self.mapGridLayout.addWidget(self.zoomButton,0,0)
        self.mapGridLayout.addWidget(self.updateButton,0,1)
        self.mapGridLayout.addWidget(self.routeData,1,0)
        self.mapGridLayout.addWidget(self.changeRoute,1,1)
        self.mapGridLayout.addWidget(self.advancedButton,2,0)
        self.mapGridLayout.addWidget(self.plotButton,2,1)
        self.zoomButton.clicked.connect(self.mapZoom)
        self.changeRoute.clicked.connect(self.createChangeWnd)
        self.routeData.clicked.connect(self.viewData)
        self.updateButton.clicked.connect(self.updateMap)
        self.advancedButton.clicked.connect(self.showAdvancedWnd)
        self.plotButton.clicked.connect(self.showPlotWnd)
        self.initUI()
    def initUI(self):
        self.setLayout(self.mapVLayout)
        self.setWindowTitle("NavigationApp")
        self.show()
    def __getPath(self):
        path=getcwd()
        path=path.replace("\\","/")
        return path
    @pyqtSlot()
    def mapZoom(self):
        self.webZView=QtWidgets.QWidget()
        self.webZLayout=QtWidgets.QHBoxLayout()
        self.zoomMap=QWebView(self.webZView)
        self.zoomMap.load(self.url)
        self.webZLayout.addWidget(self.zoomMap)
        self.webZView.setLayout(self.webZLayout)
        self.webZView.resize(1000,600)
        self.webZView.setWindowTitle("Map")
        self.webZView.show()
    @pyqtSlot()
    def createChangeWnd(self):
        title="Путь к файлу"
        path_line="Укажите путь к файлу:"
        path, okPressed = QtWidgets.QInputDialog.getText(self, title,path_line, QtWidgets.QLineEdit.Normal, "")
        if okPressed:
            self.parser=GPGGAParser(path)
            self.webMap.load(self.url)
    @pyqtSlot()
    def viewData(self):
        coord=self.parser.getCoordinates()
        deltaTimeList=self.parser.getDeltaTimeList()
        deltaDistList=self.parser.getDistList()
        speedList=self.parser.getSpeedList()
        time,dist=0,0
        self.tableLayout=QtWidgets.QVBoxLayout()
        self.tableWnd=QtWidgets.QWidget()
        self.table=QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(len(coord)-1)
        self.tableLayout.addWidget(self.table)
        self.tableWnd.setLayout(self.tableLayout)
        self.table.setHorizontalHeaderLabels(["Широта","Долгота","Расстояние(км)","Время полёта(мин)","Скорость полёта(км/ч)"])
        self.tableWnd.setWindowTitle("Данные по маршруту")
        for i in range(len(coord)-1):
            dist+=deltaDistList[i]
            time+=deltaTimeList[i]*60
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem("{0:6f}".format(coord[i][0])))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem("{0:6f}".format(coord[i][1])))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem("{0:3f}".format(dist)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem("{0:3f}".format(time)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem("{0:3f}".format(speedList[i])))
            self.table.item(i,0).setTextAlignment(Qt.AlignCenter)
            self.table.item(i,1).setTextAlignment(Qt.AlignCenter)
            self.table.item(i,2).setTextAlignment(Qt.AlignCenter)
            self.table.item(i,3).setTextAlignment(Qt.AlignCenter)
            self.table.item(i,4).setTextAlignment(Qt.AlignCenter)
        self.table.resizeColumnsToContents()
        self.tableWnd.resize(600,600)
        self.tableWnd.show()
    @pyqtSlot()
    def updateMap(self):
        self.webMap.load(self.url)
    @pyqtSlot()
    def showAdvancedWnd(self):
        self.advWnd=QtWidgets.QWidget()
        self.infoVLayout=QtWidgets.QVBoxLayout()
        self.routeLen=QtWidgets.QLabel()
        self.meanSpeed=QtWidgets.QLabel()
        self.maxHeight=QtWidgets.QLabel()
        self.minHeight=QtWidgets.QLabel()
        self.maxSpeed=QtWidgets.QLabel()
        self.minSpeed=QtWidgets.QLabel()
        self.flightTime=QtWidgets.QLabel()
        str_form="<h3>{0}({1}): {2:.3f}</h3>"
        self.routeLenStr=str_form.format("Длина маршрута","км",self.parser.getDistance())
        self.meanSpeedStr=str_form.format("Средняя скорость полета","км/ч",self.parser.getMeanSpeed())
        self.maxHeightStr=str_form.format("Максимальная высота полёта","м",self.parser.getMaxHeight())
        self.minHeightStr=str_form.format("Минимальная высота полёта","м",self.parser.getMinHeight())
        self.maxSpeedStr=str_form.format("Максимальная скорость полёта","км/ч",self.parser.getMaxSpeed())
        self.minSpeedStr=str_form.format("Минимальная скорость полёта","км/ч",self.parser.getMinSpeed())
        self.flightTimeStr=str_form.format("Время полёта","мин",self.parser.getFlightTime())
        self.maxSpeed.setText(self.maxSpeedStr)
        self.routeLen.setText(self.routeLenStr)
        self.minSpeed.setText(self.minSpeedStr)
        self.meanSpeed.setText(self.meanSpeedStr)
        self.maxHeight.setText(self.maxHeightStr)
        self.minHeight.setText(self.minHeightStr)
        self.flightTime.setText(self.flightTimeStr)
        self.infoVLayout.addWidget(self.routeLen)
        self.infoVLayout.addWidget(self.meanSpeed)
        self.infoVLayout.addWidget(self.maxSpeed)
        self.infoVLayout.addWidget(self.minSpeed)
        self.infoVLayout.addWidget(self.maxHeight)
        self.infoVLayout.addWidget(self.minHeight)
        self.infoVLayout.addWidget(self.flightTime)
        self.advWnd.setLayout(self.infoVLayout)
        self.advWnd.setWindowTitle("Дополнительно")
        self.advWnd.show()
    @pyqtSlot()
    def showPlotWnd(self):
        self.time=self.parser.getTimeList()
        self.height=self.parser.getHeightList()
        self.distance=self.parser.getDistList()
        self.coordinates=self.parser.getCoordinates()
        self.speed=self.parser.getSpeedList()
        self.plot_wnd=PlotWnd(self.time,self.speed,self.height,self.distance,self.coordinates)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())