import sqliteConnect
import pandas as pd

from TaichungBusStopDataHeader import DataHeader

headerName = DataHeader()

TaichungCityBusStopData = '臺中市市區公車站牌資料'

#region 方法

#region 行經該站的公車編號
def bueseInStop(stopInfo):
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

#endregion


desStop = "吉峰東自強路口"
takeStop = "朝陽科技大學"

# desStop = eval(input("Input Destine Stop:"))
# takeStop = eval(input("Input Take Stop:"))

tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData)

#region 目的地站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.stopName_CN, desStop)
desBusStop = sqliteConnect.selectSQL(sql)
desBusStop = dataToDict(desBusStop, tableHeader)
#endregion

#region 撘乘站
sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.stopName_CN, takeStop)
takeBusStop = sqliteConnect.selectSQL(sql)
takeBusStop = dataToDict(takeBusStop, tableHeader)
#endregion


for takeBus in takeBusStop:
    for desBus in desBusStop:
        if stopsVector(takeBus, desBus):
            print(takeBus, desBus, sep = '\n')
            print()


