#region
import pandas as pd

class stopDataModel:
    #region 欄位名稱
    def __init__(self):
        self.busID='路線' #路線：路線編號 / Stop.busID
        self.busName='路線名稱' #路線名稱：名稱為「端點A站 - 端點B站」 / Stop.busName
        self.roundTrip='方向' #方向 / Stop.roundTrip
        self.stopID='站序' #站序：發車站點（端點）為1，數字遞增為行車方向，也可稱「向量」 / Stop.stopID
        self.stopName_CN='中文站點名稱' #中文站點名稱 / Stop.stopName_CN
        self.stopName_EN='英文站點名稱' #English Stop Name / Stop.stopName_EN
        self.latitude='經度' #經度 / Stop.latitude
        self.longitude='緯度' #緯度 / Stop.longitude
        
        #路線方向分為兩種
        self.roundTrip_ob='去程' #路線名稱「端點A站 - 端點B站」為去程(outbound)，「端點A站」為發車站 / Stop.roundTrip_ob
        self.roundTrip_ib='回程' #回程(inbound)以「端點B站」發車 / Stop.roundTrip_ib
    #endregion

    #region 行經該站的公車編號
    def busesInStop(self, stopInfo):
        busID_AtStop = []
        for bus in stopInfo:
            if bus[self.busID] not in busID_AtStop:
                busID_AtStop.append(bus[self.busID])
        return busID_AtStop
    #endregion


    #region 撘乘站至目的地站
    def stopsVector(self, take, des):
        sameID = take[self.busID] == des[self.busID] # 同路線
        sameBoundRound = take[self.roundTrip] == des[self.roundTrip] # 同方向
        vector = take[self.stopID] < des[self.stopID] # 目的地站要在撘乘站之後

        return sameID and sameBoundRound and vector
    #endregion

    #region 資料轉字典
    def dataToDict(self, data, header):
        data = pd.DataFrame(data, columns = header)
        data = data.to_dict(orient = 'records')
        return data
    #endregion

    #region
    def sameBus(self, takeStopBuses, desStopBuses):
        return set(takeStopBuses) & set(desStopBuses)
    #endregion

    #region 非重覆清單，資料若已出現在清單中則不附加進
    #簡化用於去除重覆的記憶迴圈法
    def unduplicateList(self, appendToList, appendedData):
            
        if appendedData not in appendToList:
            #從未出現過才附加
            appendToList.append(appendedData)
            
    #endregion



#endregion