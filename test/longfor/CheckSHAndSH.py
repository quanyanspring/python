import requests
import json
from prettytable import PrettyTable
import datetime
import time
import xlwt
import DBConfig as config

server = "http://dbaexecsql.longfor.com/data_application/app_query/"
global a
a = 0


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


def get_count():
    global a
    return a


def set_count(id):
    global a
    a = id
    return a


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    sql_sh_acc = """
                select * from lfm_account_info where account_type = 22 and acc_no not like 'L-%' order by acc_no ;
            """

    diff_sql_sh = """
                    select *
                        from (select out_trans_no, sum(trans_amt) income
                              from t_merchant_transaction
                              where acc_no = {0}
                                and status = 1
                                and trans_type = 1
                                and target_acc_no not like 'FF%'
                                and create_time >= '2022-02-28 00:00:00'
                                and create_time < '2022-03-01 13:00:00'
                              group by out_trans_no) t
                                 left join (select order_no, sum(trans_amount) outcome
                                            from lf_account_log
                                            where account_type in (1, 2)
                                              and other_acc_no = {1}
                                              and create_time >= '2022-02-28 00:00:00'
                                              and create_time < '2022-03-01 13:00:00'
                                            group by order_no) tt on tt.order_no = t.out_trans_no
                        where t.income != tt.outcome
                   """

    while (True):

        col_list_js, row_list_js = execute_sql(sql_sh_acc, "查询商户账户", db_info[1], db_info[2])
        if row_list_js == None or len(row_list_js) == 0:
            print("商户账户为空！")
            break;

        for index, item in enumerate(row_list_js):

            sh_acc_no = item[1]

            col_list_diff, row_list_diff = execute_sql(
                diff_sql_sh.format("'" + sh_acc_no + "'", "'" + sh_acc_no + "'"), "查询商户差异", db_info[1],
                db_info[2])

            if row_list_diff != None and len(row_list_diff) != 0:
                print(row_list_diff)

        break
