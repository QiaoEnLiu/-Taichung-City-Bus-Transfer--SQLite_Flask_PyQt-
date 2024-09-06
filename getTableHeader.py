import sqliteConnect

TaichungCityBusStopData = '臺中市市區公車站牌資料'

for headerName in sqliteConnect.getHeader(TaichungCityBusStopData):
    print(headerName)

