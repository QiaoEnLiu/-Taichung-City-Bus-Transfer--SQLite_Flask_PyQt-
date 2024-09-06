import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDesktopWidget, QDialog
from PyQt5.QtCore import pyqtSlot

import Qt_UI.takeBusMainWindows_ui as main_ui

import sqliteConnect
from TaichungBusStopDataHeader import stopDataModel



#此程式碼顯示處理過的資料

TaichungCityBusStopData = '臺中市市區公車站牌資料'
theStop = stopDataModel()
tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData)



class TakeBusMainWindow(QMainWindow, main_ui.Ui_takeGUI):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.resize(800, 600)

        self.initUI()

    def initUI(self):
        self.searchButton.clicked.connect(self.searchPath)
        self.takeBusList.itemClicked.connect(self.toTF)
        self.transferStopList.itemClicked.connect(self.tfStop)

    @pyqtSlot()
    def searchPath(self):

        self.desStopName = self.desStopLineEdit.text()
        self.takeStopName = self.takeStopLineEdit.text()

        #region 目的地站
        sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.stopName_CN, self.desStopName)
        self.desBusStop = sqliteConnect.selectSQL(sql)
        self.desBusStop = theStop.dataToDict(self.desBusStop, tableHeader)
        self.desBusesID = theStop.busesInStop(self.desBusStop)

        self.desInfo = []
        for id in self.desBusesID:
            sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.busID, id)
            data = sqliteConnect.selectSQL(sql)
            data = theStop.dataToDict(data, tableHeader)
            self.desInfo.extend(data)
        #endregion

        #region 撘乘站
        sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.stopName_CN, self.takeStopName)
        self.takeBusStop = sqliteConnect.selectSQL(sql)
        self.takeBusStop = theStop.dataToDict(self.takeBusStop, tableHeader)
        self.takeBusesID = theStop.busesInStop(self.takeBusStop)

        self.takeInfo = []
        for id in self.takeBusesID:
            sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.busID, id)
            data = sqliteConnect.selectSQL(sql)
            data = theStop.dataToDict(data, tableHeader)
            self.takeInfo.extend(data)

        #endregion

        self.to_TF = []
        self.TF_to = []

        for toDes in self.desInfo:
            for fromTake in self.takeInfo:
                if toDes[theStop.stopName_CN] == fromTake[theStop.stopName_CN]:

                    theStop.unduplicateList(self.to_TF, fromTake)
                    theStop.unduplicateList(self.TF_to, toDes)

        self.to_TF_ID = theStop.busesInStop(self.to_TF)

        self.takeBusList.addItems(self.to_TF_ID)
        


    @pyqtSlot()
    def toTF(self):
        print("Select Take Bus")
        selected_Bus = self.takeBusList.selectedItems()
        if selected_Bus:
            sameStop = []
            for to_stop in self.to_TF:
                    
                if to_stop[theStop.busID] == selected_Bus[0].text():
                    for take in self.takeBusStop:
                        if theStop.stopsVector(take, to_stop):
                            theStop.unduplicateList(sameStop, to_stop[theStop.stopName_CN])

            self.transferStopList.addItems(sameStop)
        
    @pyqtSlot()
    def tfStop(self):
        print("Select Transfer Stop")
        selected_TF_Stop = self.transferStopList.selectedItems()
        if selected_TF_Stop:
            TF_Stop_to = []
            for tf in self.TF_to:
                if tf[theStop.stopName_CN] == selected_TF_Stop[0].text():
                    for des in self.desBusStop:
                        if theStop.stopsVector(tf, des):
                            theStop.unduplicateList(TF_Stop_to, tf)
            TF_to_ID = theStop.busesInStop(TF_Stop_to)
            self.transferBusList.addItems(TF_to_ID)




if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_win = TakeBusMainWindow()
    main_win.show()
    sys.exit(app.exec_())
