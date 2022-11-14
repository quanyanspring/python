import datetime
import time
import json
from prettytable import PrettyTable
import requests

server = "https://api.longhu.net/longem-migrate-prod"


# 执行sql 并查询
def execute(path, params, type='post'):
    head = {
        "Content-Type": "application/json",
        "x-gaia-api-key": "1de828d1-5105-410b-a03b-75fe1b7892f7",
        "longfor-payment-service-token": "35edbf9ce7deaf8fedae6e4f39d40523e54219ce"
    }

    params = json.dumps(params).replace("[","").replace("]","")
    print("请求参数:%s", params)

    url = server + path

    if type == 'post':
        body = invoke_post(url, head, params)
    else:
        body = invoke_get(url, params)

    try:
        json_body = json.loads(body)

        if json_body == 1:
            print("insert platform_grant_list数量为：%d" % json_body)

        elif "data" in json_body:
            if json_body["data"] != 1:
                raise RuntimeError
            print("更新数据条数:%d" % json_body["data"])
            # raise RuntimeError

    except Exception as e:
        print(url)
        print(e)
        raise TimeoutError


def get_datetime():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_str


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=params, timeout=1000, headers=head)
    return resp.text


# 请求数据
def invoke_get(url, params):
    resp = requests.get(url, data=params)
    return resp.text
