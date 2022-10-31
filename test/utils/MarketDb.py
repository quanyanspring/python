import json
import requests

server = "http://127.0.0.1:8066/queryOrderNo"

def post_lmarketing(params):
    data = {
        "list": params
    }
    head = {
        "Content-Type": "application/json"
    }

    body = invoke_post(server, head, data)


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=json.dumps(params), timeout=1000, headers=head)
    print("大会员接口响应：%s" % resp.text)
    return resp.text
