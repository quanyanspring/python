"""
项目公司流水对象
"""
from datetime import datetime
from typing import Any
import constants


class CompanyTransactionDTO:
    id: int
    targetAccNo: str
    transType: str
    transAmt: float
    businessType: str
    transTime: str
    createTime: str
    transNo: str
    accNo: str
    batchNo: str
    companyChannel: str
    activityType: str
    longminId: str
    personName: str
    personId: str
    bizSysId: str
    extra: str
    outTransNo: str
    status: int
    paymentUnitName: str
    ncCode: str
    phone: str
    createUser: str
    accName: str
    oaAccount: str

    @property
    def oaAccount(self):
        return self.oaAccount

    @oaAccount.setter
    def oaAccount(self,oaAccount):
        self.oaAccount = oaAccount


    def __init__(self, d):
        self.__dict__ = d

    def getattribute(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except:
            return None

    def setattribute(self, nam, value) -> Any:
        try:
            super().__setattr__(nam, value)
        except:
            raise TypeError

    def buildGrantList(self, activity_no, out_trans_no):
        platformGrantList = {}
        platformGrantList["batchNo"] = self.batchNo,

        platformGrantList["activityNo"] = activity_no,
        platformGrantList["walletTransNo"] = self.outTransNo,
        platformGrantList["transNo"] = self.transNo,
        if self.getattribute("activityType") is not None:
            platformGrantList["activityType"] = self.activityType,
        platformGrantList["outTransNo"] = out_trans_no,
        if self.targetAccNo.startswith("YH"):
            platformGrantList["receiverIdentity"] = 0
            platformGrantList["receiverLongminId"] = self.longminId
            if self.phone is not None:
                platformGrantList["receiverPersonPhone"] = self.phone
        else:
            if self.targetAccNo.startswith("XF"):
                platformGrantList["receiverIdentity"] = 1
            else:
                platformGrantList["receiverIdentity"] = 2
            if self.getattribute("personId") is not None:
                platformGrantList["receiverLongminId"] = self.personId
            if self.getattribute("phone") is not None:
                platformGrantList["receiverPersonPhone"] = self.phone
            if self.getattribute("oaAccount") is not None:
                platformGrantList["receiverPersonAd"] = self.oaAccount
            if self.getattribute("personName") is not None:
                platformGrantList["receiverPersonName"] = self.personName
        platformGrantList["accNoOut"] = self.targetAccNo,
        platformGrantList["businessType"] = self.businessType,
        if self.getattribute("companyChannel") is not None:
            platformGrantList["compChannel"] = self.companyChannel,
        platformGrantList["grantTime"] = self.createTime,
        platformGrantList["grantStatus"] = self.status,
        platformGrantList["grantAmount"] = self.transAmt,
        platformGrantList["createTime"] = self.createTime
        platformGrantList["modifyTime"] = datetime.now().strftime(constants.date_time_format)
        if self.getattribute("ncCode") is not None:
            platformGrantList["costBearingId"] = self.ncCode,
        if self.getattribute("paymentUnitName") is not None:
            platformGrantList["costBearingEntity"] = self.paymentUnitName,
        platformGrantList["modifyUser"] = "system_extra_6",
        platformGrantList["isDeleted"] = 0,
        return platformGrantList


if __name__ == "__main__":
     dto = CompanyTransactionDTO()
     print(dto)





