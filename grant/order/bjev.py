import json

import requests

base_url = "http://beijing-gateway-customer.app-prod.bjev.com.cn"
Authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc1JlY29tbWVuZCI6ZmFsc2UsInVzZXJfbmFtZSI6IjE1OTAxMjg1NTI4Iiwib3BlbklkIjpudWxsLCJmdWxsTmFtZSI6bnVsbCwiaXNTZXRQd2QiOmZhbHNlLCJ1c2VySWQiOjY3OTMsImNsaWVudF9pZCI6IjIwMDAwMSIsInl5VXNlcklkIjoiOGFkODRiOGM2Y2NjYjJhZTAxNmQwMzk2NDNhODM1Y2UiLCJzY29wZSI6WyJyZWFkIiwid3JpdGUiXSwiaW1Vc2VySWQiOm51bGwsImV4cCI6MTY3MDE1NDQ2NiwianRpIjoiY2YwZTdhNTctNjU1My00NTU1LWJiNjItMDQ0Y2UyNjczOWY1IiwiaXNSZWdpc3RlciI6dHJ1ZSwidXNlcm5hbWUiOiIxNTkwMTI4NTUyOCIsInRpbWVzdGFtcCI6MTY2OTU0OTY2NjczN30.YYC9YieGQxBXUHBjr9i3O9rlZKOpENG-gA4Knbdh0Y60HjhiX9XOdBRTXMQ1SG-w8bRNBMwDv2sGF-UdiSNCVfQVhnHNTNXYNZv3d22fZhhHJ2KsVjm4_f-JYLqzd2ZG9X6v0IuWu64p7uwpqn1Xa5dA1h1X9mlERWHJ_0j_9VdQYoRI8Yj3WVic2cDAK2kemGZcR7stb1GYS3IhswKfQVD-eyuxBal_vuFEax-kxYy8k8zVyJvzpju3e02Q_h7lUlVTyBRe9_tgWqnNIS5bjUsi71_9VBmpi3YAAMvNoMz_G9olT7ALBFSL9uzeB9hptN61Y6s31ozr0EpSrwMgnw"


def getHeard():
    return {
        "Authorization": Authorization,
        "Content-Type": "application/json",
        # "Content-Length": 33,
        "Cookie": "acw_tc=0bd17c2216695571248346565ed8deede0351c412f8934840852f458335b2c"
        # "Host":"beijing-gateway-customer.app-prod.bjev.com.cn",
        # "appInfo":"{\"osVersion\":\"16.1.1\",\"appType\":\"iOS\",\"appVersion\":\"3.0.1\",\"deviceName\":\"iPhone14,5\"}",
        # "User-Agent":"deviceName/iPhone%20deviceModel/iPhone14,5%20sysVersion/16.1.1"
    }

# 请求数据
def invoke_post(url, params, name="请求接口返回"):
    params = json.dumps(params)
    resp = requests.post(url, data=params, timeout=1000, headers=getHeard())
    print(name + ":" + resp.text)
    return resp.text


# 请求数据
def invoke_get(url,  name="请求接口返回"):
    resp = requests.get(url,headers = getHeard())
    print(name + ":" + resp.text)
    return resp.text

def userSignRecord(path):
    params = {
        "signType": 2,
    }
    invoke_post(base_url + path, params,"签到")

def dynamicList(path):
    invoke_get(base_url + path ,"获取文章广场")

if __name__ == "__main__":
    # 日常签到
    # userSignRecord("/beijing-zone-asset/exterior/userSignRecord/addSign")
    #获取文章广场
    dynamicList("/beijing-zone-dynamic/exterior/dynamic/list?pageIndex=1&pageSize=20")
