#region
class DataHeader:
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

#endregion