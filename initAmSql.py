import datetime
import time
import json
from prettytable import PrettyTable
import requests

url = "https://api.longhu.net/iam-openapi/public/v3/role/getByKeyword"


# 执行sql 并查询
def execute_sql(keyworld):
    start_cond = time.time()
    head = {
        "X-Gaia-Api-Key": "c3dcc477-249a-4f26-9d72-b2cf6f0b6d19",
        "Content-Type": "application/json"
    }
    # 请求数据
    data = {
        "keyword": keyworld,
        "roleType": 0,
        "exactMatch": "false",
    }
    body = invoke_post(url, head, data)
    json_body = json.loads(body)
    cost_time = str((time.time() - start_cond))


def get_datetime():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_str


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=params, timeout=1000, headers=head)
    return resp.text


# tidb 数据查询
def execute_tidb_sql(sql, instance="tidb10.31.48.7_脱敏查询", db_name="longem_tidb", detail="query"):
    return execute_sql(sql, detail, instance, db_name)


if __name__ == "__main__":

    keyword_list = {
        "集团-赋能平台-大会员及珑珠-珑珠-发放结算对接人",
        "C1-项目-财务-项目财务经理",
        "C1-地区-财务-财务管理-员工",
        "C2-项目-项目财务经理",
        "C2-地区-商业财务-员工",
        "C1-地区-财务-创新业务财务-财务经理",
        "C4-地区-财务-员工",
        "C5-地区-财务-员工",
        "C6-地区-财务-员工",
        "C1-地区-财务-创新业务财务-财务经理",
        "C1-地区-财务-财务管理-员工",
        "ST-电银_财务-员工",
        "ST-飞鸟鱼-财务-财务分析主管 ",
        "ST-双湖-财务-财务专员"
    }

    for index,item in enumerate(keyword_list):
        print("index:%s,角色：%s".format(index,item))
        execute_sql(item)
