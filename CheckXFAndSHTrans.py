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

    # diff_sql_sh = """
    #             select * from t_merchant_transaction where status = 5 and id > {0} order by id asc;
    #         """
    #
    # diff_sql_xf = """
    #             select
    #             (select acc_out_amt from t_transaction where out_trans_no = {0} and acc_out like 'XF%' and acc_in like 'SH%')-
    #             (select acc_out_amt from t_transaction where remark3 = {1} and acc_out like 'SH%' and acc_in like 'XF%')
    #         """

    diff_sql_sh = """
                   select * from t_merchant_transaction  where  acc_no  = 'SH-201222-000405' and create_time > '2022-02-10' and  create_time < '2022-02-11' and target_acc_no not like 'FF%' and target_acc_no not like 'SH%'  and id > {0} order by id ;
               """

    diff_sql_lf = """
                    select * from lf_account_log where order_no in {0};
                   """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    yh_count = 2147483647;
    for i in range(yh_count):

        diff_sql_sh = diff_sql_sh.format(get_count())
        col_list_sh, row_list_sh = execute_sql(diff_sql_sh, "查询商户流水", db_info[1], db_info[2])
        if row_list_sh == None or len(row_list_sh) == 0:
            print("商户流水为空！")
            break;

        set_count(row_list_sh[len(row_list_sh) - 1][0])

        for index,item in enumerate(row_list_sh):

            out_trans_no = item[3]
            status = item[24]
            trans_type = item[16]

            if status == 5:
                pass
            if trans_type == 2:
                original_no = item[4]
                diff_sql_lf = diff_sql_lf.format("('" + out_trans_no + "'," + "'" + original_no + "')")
            else:
                diff_sql_lf = diff_sql_lf.format("('" + out_trans_no + "')")

            col_list_lf, row_list_lf = execute_sql(diff_sql_lf, "查询用户流水", db_info[1], db_info[2])

            if row_list_lf == None or len(row_list_lf) == 0:
                print("用户流水为空！"+ out_trans_no)

            set_count(row_list_sh[len(row_list_sh) - 1][0])
            # print(get_count())
            trans_amt = item[8]

            if  status == 5:
                if len(row_list_lf) != 2:
                    print("取消订单错误：" + out_trans_no)

            if status == 1:
                if trans_type == 1:
                    if len(row_list_lf) != 1:
                        print("消费订单错误：" + out_trans_no)
                if trans_type == 2:
                    if len(row_list_lf) != 2:
                        print("退款订单错误：" + out_trans_no)

            diff_sql_lf = """
                select * from lf_account_log where order_no in {0};
            """

        diff_sql_sh = """
                           select * from t_merchant_transaction  where  acc_no  = 'SH-201222-000405' and create_time > '2022-02-10' and  create_time < '2022-02-11' and target_acc_no not like 'FF%' and target_acc_no not like 'SH%'  and id > {0} order by id ;
                       """