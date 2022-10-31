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
        "Cookie": "zg_87d550a769cd4f4995a2da640d7869f7=%7B%22sid%22%3A%201639576658776%2C%22updated%22%3A%201639576664352%2C%22info%22%3A%201639576658779%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E9%BE%99%E4%BF%A13.0%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Foriginal-nas-pro.longfor.com%2Foriginal-nas-pro%2FapplicationMedia%2F1637227663740.html%3FExpires%3D1952587666%26OSSAccessKeyId%3DLTAI4Fw2dUgQvkWHnasff6ps%26Signature%3DiAnb9ursRD5lBbMig6hjQTZ7cGc%253D%23%2Fmain%2Fportal%2Fportal-1-1%22%7D; csrftoken=JkqBk4Hs0fa7WS6iV5VJkUxSLl32aA512JQnVHmDHDI2GBMzvdJPe8lXdeui1qAE; CASTGC=TGT-18135-Z97atyO-i261eEpYO2nvxcGgc7WTa6OnlFKsB5rXL56T0M4WKeNZNl9nGIEXa4f2zyM-longhu; account=TGT-18135-Z97atyO-i261eEpYO2nvxcGgc7WTa6OnlFKsB5rXL56T0M4WKeNZNl9nGIEXa4f2zyM-longhu; sessionid=rqy14o0uwj90umuob69c3p2t6ikkdzzf",
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

    sql_js = """
                   select merchant_no from lfm_account_info where account_type = 21 group by merchant_no;
               """
    diff_sql_js = """
                    select ff.amount inAmt, js.amount outAmt, (ff.amount + js.amount) result, ff.merchant_no
                    from (select sum(if(action_type in (3, 4, 8), trans_amount, -trans_amount)) amount, merchant_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type != 25
                            and merchant_no = {0}
                          group by merchant_no) ff
                             left join (select sum(if(action_type = 3, trans_amount, -trans_amount)) amount, merchant_no
                                        from lfm_account_log
                                        where account_type = 21
                                          and other_account_type in (20,21)
                                          and action_type != -1
                                          and action_type != 11
                                          and merchant_no = {1}
                                          and business_type != '041'
                                          and business_type != '079'
                                        group by merchant_no) js on js.merchant_no = ff.merchant_no
                    having result != 0;
                   """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    whileFlag = True
    while (whileFlag):

        col_list_js, row_list_js = execute_sql(sql_js, "查询结算账户", db_info[1], db_info[2])
        if row_list_js == None or len(row_list_js) == 0:
            print("结算账户为空！")
            break;

        for index, item in enumerate(row_list_js):

            js_acc_no = item[0]

            col_list_diff, row_list_diff = execute_sql(
                diff_sql_js.format("'" + js_acc_no + "'", "'" + js_acc_no + "'"), "查询结算差异", db_info[1],
                db_info[2])

            if row_list_diff != None and len(row_list_diff) != 0:
                try:
                    js_diff = row_list_diff[0]
                    print(js_diff)
                    amount = js_diff[2]
                    if amount != 0:
                        print("error")
                except Exception as e:
                    print(e)


        break
