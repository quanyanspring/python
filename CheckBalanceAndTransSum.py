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


# tidb 数据查询
def execute_sql(sql, detail, instance, db_name, limit_num=1000):
    return execute(sql, detail, instance, db_name, limit_num)


# 执行sql 并查询
def execute(sql, detail, instance, db_name, limit_num):
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
        "limit_num": limit_num
    }
    # print("start migrate trans ")
    body = invoke_post(server, head, data)
    json_body = json.loads(body)
    cost_time = str((time.time() - start_cond))

    # print(json_body)
    # 处理成功的情况
    if "status" in json_body and "data" in json_body:
        msg = json_body["msg"]
        print(msg)

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
            # print(detail + " 校验不通过 cost_time " + cost_time)

        tb = PrettyTable()  # 生成表格对象
        tb.field_names = col_list  # 定义表头

        for nd in row_list:
            tb.add_row(nd)  # 添加一行，列是column

        print("")
        print(tb)
        #  print("total line {}".format(len(row_list)))
        return col_list, row_list


def get_count():
    global a
    print(a)
    a = a + 1
    return a


if __name__ == "__main__":

    db_info = config.db_list_info[0]

    xf_account_sql = """
        select * from lf_account where account_type = 1 order by acc_no ;
        """

    xf_sum_sql = """
        select IFNULL(SUM(IF(action_type in (1, 4, 5, 6, 8), trans_amount, -trans_amount)), 0),acc_no from lf_account_log  where account_type = 1 and acc_no = {accNo} group by acc_no
        """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    for i in range(1):

        # 查询账户信息
        col_list, row_list = execute_sql(xf_account_sql, "查询账户", db_info[1], db_info[2], 10)

        if len(row_list) == 0:
            break

        if len(col_list) > 0 and len(row_list) > 0:

            # 标题列
            if get_count() == 1:
                print("写入标题列")
                worksheet.write(0, 0, "sum_balance")
                for i in range(len(col_list)):
                    col_str = col_list[i]
                    worksheet.write(0, i + 1, col_str)

            for j in range(len(row_list)):
                row = row_list[j]
                acc_no = row[1]
                balance_amt = row[6]

                print("处理账户：", row[0])

                # 查询账户总金额
                sql = xf_sum_sql.format(accNo="'" + acc_no + "'")
                col_list_acc, row_list_acc = execute_sql(sql, "查询账户总金额", db_info[1], db_info[2])

                if col_list_acc and row_list_acc:
                    sum_balance = row_list_acc[0][0]

                    print("账户：{0}，余额：{1}，流水总金额：{2}".format(acc_no, balance_amt, sum_balance))

                    if sum_balance:
                        if balance_amt != sum_balance:

                            row_count = get_count() - 1
                            print("开始写入错误数据")
                            # 错误数据列
                            for j in range(len(row)):
                                val = row[j]
                                if j == 0:
                                    worksheet.write(row_count, 0, sum_balance)
                                else:
                                    worksheet.write(row_count, j + 1, val)

            time.sleep(1)

    # 保存文件
    workbook.save('/Users/admin/Desktop/大等式/账户余额和流水总额比较.xls')
