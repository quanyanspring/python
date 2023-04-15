import json

import requests
import time
import random

base_url = "http://beijing-gateway-customer.app-prod.bjev.com.cn"
Authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc1JlY29tbWVuZCI6ZmFsc2UsInVzZXJfbmFtZSI6IjE1OTAxMjg1NTI4Iiwib3BlbklkIjpudWxsLCJmdWxsTmFtZSI6bnVsbCwiaXNTZXRQd2QiOmZhbHNlLCJ1c2VySWQiOjY3OTMsImNsaWVudF9pZCI6IjIwMDAwMSIsInl5VXNlcklkIjoiOGFkODRiOGM2Y2NjYjJhZTAxNmQwMzk2NDNhODM1Y2UiLCJzY29wZSI6WyJyZWFkIiwid3JpdGUiXSwiaW1Vc2VySWQiOm51bGwsImV4cCI6MTY3Mjc0ODgzOCwianRpIjoiOGE1MjM1MDgtMmU5OS00ZDhkLWE5MzktNzVmZTA3ZGI1MzE2IiwiaXNSZWdpc3RlciI6dHJ1ZSwidXNlcm5hbWUiOiIxNTkwMTI4NTUyOCIsInRpbWVzdGFtcCI6MTY3MDE1NjgzODQwNX0.UjUFXGpilsOZtzLAJQ7uxu4_u9DmMFfOQiYbfiqUrOUMVHdgjgIl3_iOCQa59mvVWzhNbp0uKlsvLhG1213w1Rp6hSlqnrmYKbB7aelXEFmizOg513AKY9iMuj6OOsGUx0MrSWVjKkpkmen4gp5QEUFqJ2wqK6728Lm_RfMPExehnrwtHay26lCDO24znSVSLM6wrGoDpsZlH7LrKYf17ym8LHk92t2RvzCEllDf1uT08gyWdzA0TQ4eiHQ_o4w9kIjqFGDUBId9ulgxdcDuM1E3cK4hCmhnz1ardOb_4gxI9HchmWDQDnPlAebZdPjbGh0fw9fUaK7m71e87V7J8Q"
myUserId = ""


def getHeard():
    return {
        "Authorization": Authorization,
        "Content-Type": "application/json",
        "Cookie": ""
    }


# 请求数据
def invoke_post(url, params, name="请求接口返回"):
    params = json.dumps(params)
    resp = requests.post(base_url + url, data=params, timeout=1000, headers=getHeard())
    print(name + ":" + resp.text)
    time.sleep(random.randint(3, 6))
    return resp.text


# 请求数据
def invoke_post_default(url, params, name="请求接口返回"):
    params = json.dumps(params)
    resp = requests.post(url, data=params, timeout=1000, headers=getHeard())
    print(name + ":" + resp.text)
    time.sleep(random.randint(3, 6))
    return resp.text


# 请求数据
def invoke_get(url, name="请求接口返回"):
    resp = requests.get(base_url + url, headers=getHeard())
    print(name + ":" + resp.text)
    time.sleep(random.randint(3, 6))
    return resp.text


# 请求数据
def invoke_get_default(url, name="请求接口返回"):
    resp = requests.get(url, headers=getHeard())
    print(name + ":" + resp.text)
    time.sleep(random.randint(3, 6))
    return resp.text


# 签到
def userSignRecord(path):
    params = {
        "signType": 2,
    }
    invoke_post(path, params, "签到")


# 点赞次数、分享次数、关注、点赞自己
global liked, shared, followed, my_liked
liked = 1
shared = 1
followed = 1
my_liked = 1


# 点赞
def like(entityId):
    params = {
        "type": 2,
        "commentId": "",
        "entityId": entityId
    }
    invoke_post("/beijing-zone-dynamic/exterior/interact/like", params, "点赞")


# 分享
def share(entityId):
    params = {
        "entityType": 2,
        "entityId": entityId
    }
    invoke_post("/beijing-zone-dynamic/exterior/interact/dynamic/share", params, "分享")


# 关注
def followings(userId):
    params = {

    }
    followings_path = "https://api.smartservice.bjev.com.cn/gateway-api/v1/users/{0}/followings/{1}".format(userId,
                                                                                                            myUserId)
    invoke_post_default(followings_path, params,"关注")


fans_User_id_list = []


# 粉丝列表
def fans(pageIndex=1, pageSize=20):
    fans_path = "https://api.smartservice.bjev.com.cn/gateway-api//v1/users/{0}/follows?page={1}&page.size={2}".format(
        myUserId,
        pageIndex, pageSize)
    fans_resp = invoke_get_default(fans_path,"获取粉丝列表")
    fans_js = json.loads(fans_resp)
    if "content" in fans_js:
        totalPages = fans_js["totalPages"]
        content = fans_js["content"]
        for con in content:
            fans_User_id_list.append(con["member"]["userId"])
        if pageIndex < totalPages:
            # 递归
            fans(pageIndex + 1, pageSize)


context_list = []


# 自己文章
def myContext(pageIndex=1, pageSize=20):
    global my_liked
    my_context_path = "/beijing-zone-dynamic/exterior/dynamic/list?isRecommend=1&otherUserId={0}&pageIndex={1}&pageSize={2}".format(
        myUserId, pageIndex, pageSize)
    context_list = invoke_get(my_context_path, "我的文章列表")
    context_js = json.loads(context_list)
    if "data" in context_js:
        data = context_js["data"]
        for txt in data["dataList"]:
            id_ = txt["id"]
            if my_liked < 3:
                if txt["liked"] != 1:
                    # 点赞自己
                    #like(id_)
                    my_liked += 1
            else:
                break
        # 递归
        if my_liked < 3:
            myContext(pageIndex + 1, pageSize)


# 收积分
def receiveAward(value,name):
    params = {
        "taskGroupCode": value
    }
    invoke_post("/beijing-zone-asset/exterior/userTaskProgress/receiveAward", params, f"收积分:{name}")


# 查询文章列表并点赞
def dynamicList(pageIndex=1, pageSize=20):
    global liked
    global shared
    global followed
    dynamic_path = "/beijing-zone-dynamic/exterior/dynamic/list?pageIndex={0}&pageSize={1}".format(pageIndex, pageSize)
    resp = invoke_get(dynamic_path, "获取文章广场")
    resp_js = json.loads(resp)
    if "data" in resp_js:
        data_ = resp_js["data"]

        for col in data_["dataList"]:
            id = col["id"]
            userId = col["createUser"]["userId"]
            # 点赞
            if col["liked"] == -1:
                like(id)
                liked += 1
            if liked >= 6:
                break

            # 分享
            if shared < 3:
                share(id)
                shared += 1

            # 关注
            if not fans_User_id_list.__contains__(userId):
                if followed < 3:
                    followings(userId)
                    followed += 1

        if liked <= 5:
            # 递归查询列表
            dynamicList(pageIndex + 1, pageSize)
    else:
        print("查询列表错误")


if __name__ == "__main__":
    # 日常签到
    userSignRecord("/beijing-zone-asset/exterior/userSignRecord/addSign")
    # 粉丝列表
    fans()
    # 获取文章广场并点赞、分享、关注
    dynamicList()
    # 点赞收积分
    receiveAward("ENTITY_LIKE","点赞")
    # 分享收积分
    receiveAward("ENTITY_SHARE","分享")
    # 关注收积分
    receiveAward("GET_TASK_ATTENTION","关注")
    # 被别人点赞收积分
    receiveAward("GET_TASK_LIKE","被点赞")
