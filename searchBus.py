import sqliteConnect
import pandas as pd


from TaichungBusStopDataHeader import DataHeader

headerName = DataHeader()

TaichungCityBusStopData = '臺中市市區公車站牌資料'
tableHeader = sqliteConnect.getHeader(TaichungCityBusStopData) # 欄位名稱

searchBus = eval(input("Search Taichung Bus:"))

sql = "SELECT * FROM {} WHERE {} = '{}'".format(TaichungCityBusStopData, headerName.busID, searchBus)
busLine = sqliteConnect.selectSQL(sql)
busLine = pd.DataFrame(busLine, columns = tableHeader)
busLine = busLine.to_dict(orient = 'records')

for stop in busLine:
    print(stop)

