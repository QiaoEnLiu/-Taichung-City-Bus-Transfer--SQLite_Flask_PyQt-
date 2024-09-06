import sqliteConnect

from TaichungBusStopDataModel import stopDataModel

theStop = stopDataModel()

TaichungCityBusStopData = '臺中市市區公車站牌資料'
# TaichungCityBusStopData = '測試資料集'



desStopName = "逢甲大學(福星路)"
takeStopName = "吉峰東自強路口"

# desStopName = str(input("Input Destine Stop: "))
# takeStopName = str(input("Input Take Stop: "))

tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData)

#region 目的地站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.stopName_CN, desStopName)
desBusStop = sqliteConnect.selectSQL(sql)
desBusStop = theStop.dataToDict(desBusStop, tableHeader)
desBusesID = theStop.busesInStop(desBusStop)

desInfo = []
for id in desBusesID:
    sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.busID, id)
    data = sqliteConnect.selectSQL(sql)
    data = theStop.dataToDict(data, tableHeader)
    desInfo.extend(data)
#endregion

#region 撘乘站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.stopName_CN, takeStopName)
takeBusStop = sqliteConnect.selectSQL(sql)
takeBusStop = theStop.dataToDict(takeBusStop, tableHeader)
takeBusesID = theStop.busesInStop(takeBusStop)
# print(takeBusesID)

takeInfo = []
for id in takeBusesID:
    sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, theStop.busID, id)
    data = sqliteConnect.selectSQL(sql)
    data = theStop.dataToDict(data, tableHeader)
    takeInfo.extend(data)

# for stop in takeInfo:
#     print(stop)

#endregion

to_TF = []
TF_to = []

for toDes in desInfo:
    for fromTake in takeInfo:
        if toDes[theStop.stopName_CN] == fromTake[theStop.stopName_CN]:

            theStop.unduplicateList(to_TF, fromTake)
            theStop.unduplicateList(TF_to, toDes)


# for stop in to_TF:
#     print(stop)


to_TF_ID = theStop.busesInStop(to_TF)

# print(to_TF_ID)

print()
selectTakeBus = str(input("Bus at {}\n{}\nSearch Bus: ".format(takeStopName, to_TF_ID) or to_TF_ID[0]))

sameStop = []
for to_stop in to_TF:
        
    if to_stop[theStop.busID] == selectTakeBus:
        for take in takeBusStop:
            if theStop.stopsVector(take, to_stop):
                theStop.unduplicateList(sameStop, to_stop[theStop.stopName_CN])

# print(sameStop)

print()
selectTransferStop = str(input("Transfer Stop {}\nSelect Transfer Stop: ".format(sameStop) or sameStop[0]))

TF_Stop_to = []
for tf in TF_to:
    if tf[theStop.stopName_CN] == selectTransferStop:
        for des in desBusStop:
            if theStop.stopsVector(tf, des):
                theStop.unduplicateList(TF_Stop_to, tf)
TF_to_ID = theStop.busesInStop(TF_Stop_to)

print()
selectBusToDes = str(input("At {}\nSelect Bus {}: ".format(selectTransferStop, TF_to_ID) or TF_to_ID[0]))

print(takeStopName, selectTakeBus, selectTransferStop, selectBusToDes, desStopName, sep = "\n")
        





