import config.server_config as cof
import requests
import json
from prettytable import PrettyTable
import datetime
import time

server = "http://dbaexecsql.longfor.com/data_application/app_query/"


def get_datetime():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_str


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=params, timeout=1000, headers=head)
    return resp.text

# tidb 数据查询
def execute_tidb_sql(sql, instance="tidb10.31.48.7_脱敏查询",db_name = "longem_tidb", detail="query"):
    return execute_sql(sql, detail, instance, db_name)

# 执行sql 并查询
def execute_sql(sql, detail, instance, db_name):
    start_cond = time.time()
    head = {
        "Cookie": cof.sql_cookie,
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
        "limit_num": 1000
    }
    # print("start migrate trans ")
    body = invoke_post(server, head, data)
    json_body = json.loads(body)
    end_cond = time.time()
    cost_time = str((end_cond - start_cond))

    # print(json_body)
    # 处理成功的情况
    if "status" in json_body and "data" in json_body:
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
            print(detail + " 校验通过 cost_time " + cost_time)
            return col_list, None
        else:
            pass
            # print("{} execute sql \n{} \ncost time {}\n error {}".format(get_datetime(), full_sql, query_time, error))
            #print(detail + " 校验不通过 cost_time " + cost_time)

        tb = PrettyTable()  # 生成表格对象
        tb.field_names = col_list  # 定义表头

        for nd in row_list:
            tb.add_row(nd)  # 添加一行，列是column

        print("")
        # print(tb)
       #  print("total line {}".format(len(row_list)))
        return col_list, row_list


db_list_info = [
    ["tidb数据库", "tidb10.31.48.7_脱敏查询", "longem_tidb"],
    ["C端C1库", "10.31.54.176_脱敏查询", "longgem_caccount_c1"],
    ["C端C0库", "10.31.54.177_脱敏查询", "longgem_caccount_c0"],
    ["B端库", "10.31.54.213_脱敏查询", "longgem_baccount"],
    ["前置数据库", "10.31.54.11_脱敏查询", "longgem_integrate"]
]

if __name__ == "__main__":

    db_info = db_list_info[2]
    sql = """
    select * from lf_account_log_2021_9  where user_id = "10188528"  limit 2
    """

    col_list, row_list = execute_sql(sql, "生成数据", db_info[1], db_info[2])
    if col_list and row_list:

        insert_sql = "insert into lf_account_log "

        col_data_list = ["`" + col_list[i] + "`" for i in range(len(col_list))]
        col_str = ",".join(col_data_list)
        # print(col_str)

        val_list = ""
        for i in range(len(row_list)):
            row = row_list[i]
            tmp_str_list = []
            for j in range(len(row)):
                val = row[j]
                if val == None:
                    tmp_str_list.append("")
                else:
                    tmp_str_list.append("'" + str(val) + "'")
            tmp_str = ",".join(tmp_str_list)
            # print(tmp_str)
            val_list += "(" + tmp_str + "),"
        val_list = val_list[0:-1] + ";"

        result_sql = insert_sql + "(" + col_str + ") VALUES " +val_list
        print(result_sql)