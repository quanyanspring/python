import datetime
import time
import json
from prettytable import PrettyTable
import requests
import pymysql

server = "http://dbaexecsql.longfor.com/data_application/app_query/"


def execute_select_sql_uat(sql, db_config):
    # db = pymysql.connect(host="10.31.99.227",port=3306, user="root", password="123456aA!", database="uat_wallet")
    try:
        db = pymysql.connect(host=db_config[1],
                             port=db_config[2],
                             user=db_config[3],
                             password=db_config[4],
                             database=db_config[5]
                             )
    except Exception as e:
        print("连接不成功！")
        print(e)
        raise Exception("连接不成功", e)
    cursor = db.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    print("结果集:", str(len(fetchall)), "个")
    return fetchall


def execute_update_sql_uat(sql, db_config):
    try:
        db = pymysql.connect(host=db_config[1],
                             port=db_config[2],
                             user=db_config[3],
                             password=db_config[4],
                             database=db_config[5]
                             )
    except Exception as e:
        print("连接不成功！")
        print(e)
        raise Exception("连接不成功", e)
    cursor = db.cursor()
    execute = cursor.execute(sql)
    db.commit()
    return execute


# 执行sql 并查询
def execute_sql(sql, detail, instance, db_name):
    start_cond = time.time()
    head = {
        "Cookie": "",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    # 去除换行
    sql = " ".join(sql.strip().split("\n"))
    # 请求数据
    data = {
        "instance_name": instance,
        "db_name": db_name,
        "schema_name": "",
        "tb_name": "",
        "sql_content": sql,
        "limit_num": 10000
    }
    # print("start migrate trans ")
    body = invoke_post(server, head, data)
    json_body = json.loads(body)
    cost_time = str((time.time() - start_cond))

    # print(json_body)
    # 处理成功的情况
    if "status" in json_body and "data" in json_body:
        msg = json_body["msg"]
        # print(msg)

        data_cont = json_body["data"]
        if "column_list" not in data_cont:
            print("\n" + sql)
            return None, None

        col_list = data_cont["column_list"]
        row_list = data_cont["rows"]
        full_sql = data_cont["full_sql"]
        error = data_cont["error"]
        query_time = data_cont["query_time"]

        if len(row_list) == 0:
            # print(detail + " 校验通过 cost_time " + cost_time)
            return col_list, None
        else:
            pass
            # print("{} execute sql \n{} \ncost time {}\n error {}".format(get_datetime(), full_sql, query_time, error))
            # print(detail + " 校验不通过 cost_time " + cost_time)

        tb = PrettyTable()  # 生成表格对象
        tb.field_names = col_list  # 定义表头

        for nd in row_list:
            tb.add_row(nd)  # 添加一行，列是column

        print("")
        # print(tb)
        #  print("total line {}".format(len(row_list)))
        return col_list, row_list


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
