import sqliteConnect
import pandas as pd

from TaichungBusStopDataHeader import DataHeader

headerName = DataHeader()

TaichungCityBusStopData = '臺中市市區公車站牌資料'

# searchStop = eval(input("Search Taichung Stop:"))
searchStop = "朝陽科技大學"
tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData) # 欄位名稱

sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.stopName_CN, searchStop)
busStop = sqliteConnect.selectSQL(sql)
busStop = pd.DataFrame(busStop, columns = tableHeader)
busStop = busStop.to_dict(orient = 'records')

for stop in busStop:
    print(stop)

#region 該站上的公車
busInStop = []
for bus in busStop:
    if bus[headerName.busID] not in busInStop:
        busInStop.append(bus[headerName.busID])
print(busInStop)
#endregion

