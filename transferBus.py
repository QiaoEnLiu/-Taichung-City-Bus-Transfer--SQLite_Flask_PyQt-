import sqliteConnect
import pandas as pd

from TaichungBusStopDataHeader import DataHeader

headerName = DataHeader()

# TaichungCityBusStopData = '臺中市市區公車站牌資料'
TaichungCityBusStopData = '測試資料集'

#region 方法

#region 行經該站的公車編號
def busesInStop(stopInfo):
    busID_AtStop = []
    for bus in stopInfo:
        if bus[headerName.busID] not in busID_AtStop:
            busID_AtStop.append(bus[headerName.busID])
    return busID_AtStop
#endregion

#region 撘乘站至目的地站
def stopsVector(take, des):
    sameID = take[headerName.busID] == des[headerName.busID] # 同路線
    sameBoundRound = take[headerName.roundTrip] == des[headerName.roundTrip] # 同方向
    vector = take[headerName.stopID] < des[headerName.stopID] # 目的地站要在撘乘站之後

    return sameID and sameBoundRound and vector
#endregion


#region 資料轉字典
def dataToDict(data, header):
    data = pd.DataFrame(data, columns = header)
    data = data.to_dict(orient = 'records')
    return data
#endregion

#region 非重覆清單，資料若已出現在清單中則不附加進
#簡化用於去除重覆的記憶迴圈法
def unduplicateList(appendToList, appendedData):
        
    if appendedData not in appendToList:
        #從未出現過才附加
        appendToList.append(appendedData)
        
#endregion

#endregion


desStopName = "逢甲大學(福星路)"
takeStopName = "吉峰東自強路口"

# desStopName = str(input("Input Destine Stop: "))
# takeStopName = str(input("Input Take Stop: "))

tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData)

#region 目的地站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.stopName_CN, desStopName)
desBusStop = sqliteConnect.selectSQL(sql)
desBusStop = dataToDict(desBusStop, tableHeader)
desBusesID = busesInStop(desBusStop)

desInfo = []
for id in desBusesID:
    sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.busID, id)
    data = sqliteConnect.selectSQL(sql)
    data = dataToDict(data, tableHeader)
    desInfo.extend(data)
#endregion

#region 撘乘站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.stopName_CN, takeStopName)
takeBusStop = sqliteConnect.selectSQL(sql)
takeBusStop = dataToDict(takeBusStop, tableHeader)
takeBusesID = busesInStop(takeBusStop)
# print(takeBusesID)

takeInfo = []
for id in takeBusesID:
    sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.busID, id)
    data = sqliteConnect.selectSQL(sql)
    data = dataToDict(data, tableHeader)
    takeInfo.extend(data)

for stop in takeInfo:
    print(stop)

#endregion

to_TF = []
TF_to = []

for toDes in desInfo:
    for fromTake in takeInfo:
        # print(toDes[headerName.stopName_CN], fromTake[headerName.stopName_CN], toDes[headerName.stopName_CN] == fromTake[headerName.stopName_CN])
        if toDes[headerName.stopName_CN] == fromTake[headerName.stopName_CN]:

            unduplicateList(to_TF, fromTake)
            unduplicateList(TF_to, toDes)


# for stop in to_TF:
#     print(stop)

print(to_TF)


to_TF_ID = busesInStop(to_TF)

# print(to_TF_ID)

print()
selectTakeBus = str(input("Bus at {}\n{}\nSearch Bus: ".format(takeStopName, to_TF_ID) or to_TF_ID[0]))

sameStop = []
for to_stop in to_TF:
        
    if to_stop[headerName.busID] == selectTakeBus:
        for take in takeBusStop:
            if stopsVector(take, to_stop):
                unduplicateList(sameStop, to_stop[headerName.stopName_CN])

# print(sameStop)

print()
selectTransferStop = str(input("Transfer Stop {}\nSelect Transfer Stop: ".format(sameStop) or sameStop[0]))

TF_Stop_to = []
for tf in TF_to:
    if tf[headerName.stopName_CN] == selectTransferStop:
        for des in desBusStop:
            if stopsVector(tf, des):
                unduplicateList(TF_Stop_to, tf)
TF_to_ID = busesInStop(TF_Stop_to)

print()
selectBusToDes = str(input("At {}\nSelect Bus {}: ".format(selectTransferStop, TF_to_ID) or TF_to_ID[0]))

print(takeStopName, selectTakeBus, selectTransferStop, selectBusToDes, desStopName, sep = "\n")
        





