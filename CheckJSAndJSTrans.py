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
        "Cookie": "CASTGC=TGT-157311-flyy1RHetVPdemYeqStQvYDH4-F2LjuOCbl702K0AvN-KcBtcJ85qJ2n7pF-FRhB7SE-longhu; account=TGT-157311-flyy1RHetVPdemYeqStQvYDH4-F2LjuOCbl702K0AvN-KcBtcJ85qJ2n7pF-FRhB7SE-longhu; sessionid=ago8dc6umajqvqnkbeluktq5yt87m423; IM-Access-Token=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4MjdjZjVkMC1lNzVlLTQ0YTItYjNmOC0wMGE5NGMxNWE2NDEiLCJpc3MiOiJkcmFnb25sZXR0ZXIzLjAiLCJzdWIiOiJ7XCJ1c2VyTmFtZVwiOlwid2FuZ2xpbnF1YW5cIixcInVzZXJJZFwiOlwiNjAwMDMyOTE5XCJ9IiwiaWF0IjoxNjQ0ODkwMDYyLCJleHAiOjE2NDQ5NzY0NjJ9.g9nujIPE92V6WH-C7yHD87-kvzLp5iP4xr6SX_iSFo0; rd_pic_tkn=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZWFsTmFtZSI6IueOi-ael-WFqCIsInVzZXJJbmZvIjoie1wicG9ydHJhaXRVcmxcIjpcImh0dHBzOi8vcHJvZC1sb25neGluLW9zcy5vc3MtY24tYmVpamluZy5hbGl5dW5jcy5jb20vb3JpZ2luYWwtbmFzLXByby9oZWFkSW1nezF9NjAwMDMyOTE5LmpwZz9oZWFkSWQ9MTAwMDFcIixcInNleFwiOjEsXCJkZXB0SW5mb1wiOlt7XCJkZXB0c1wiOlt7XCJiaXpJZFwiOlwiMTAwMDAwMDAwM1wiLFwibmFtZVwiOlwi6b6Z5rmW6ZuG5ZuiXCJ9LHtcImJpeklkXCI6XCIxMDAwMDAwMDcxXCIsXCJuYW1lXCI6XCLmlbDlrZfnp5HmioDpg6hcIn0se1wiYml6SWRcIjpcIjYwMDAwNDU2ODhcIixcIm5hbWVcIjpcIuWkp-S8muWRmOWSjOePkeePoOWboumYn1wifSx7XCJiaXpJZFwiOlwiNjAwMDE2OTk1NFwiLFwibmFtZVwiOlwi5oqA5pyv5Zui6ZifXCJ9LHtcImJpeklkXCI6XCI2MDAwMTY5OTYxXCIsXCJuYW1lXCI6XCLmnrbmnoTnu4RcIn1dLFwiaXNNYWluXCI6MSxcImpvYlwiOlwi5p625p6E5ZGY5belXCJ9XX0iLCJleHBpcmVUaW1lIjoxNjQ0OTc2NDYyOTc3LCJyb2xlQ29kZSI6IjEiLCJpc3MiOiLnjovmnpflhagiLCJ1c2VySWQiOiJ3YW5nbGlucXVhbiIsImZpbGVJZCI6ImU1RnY5aVRzUUhHUkxNc2hObEg1Y05FeU5UeTkifQ.PAYifcJJlBgBtQXF2L675uZQdAnFKcrP5lu8sCCodQA",
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
                   select acc_no from lfm_account_info where acc_no like 'JS%';
               """
    diff_sql_js = """
                    select lai.acc_no, (ifnull(t.amt,0) - j.balance - j.settle_amount) result
                    from lfm_account_balance j
                             join lfm_account_info lai on j.account_id = lai.account_id
                             left join (select sum(if(action_type in (1, 3, 4, 6, 8), trans_amount, -trans_amount)) amt, acc_no
                                        from lfm_account_log
                                        where acc_no = {accNo}
                                          and other_account_type in (20,21)
                                          and action_type in (0, 1, 2, 3, 4, 6, 7, 8,11)
                                          and order_no not like 'DLX%'
                                        group by acc_no) t on t.acc_no = lai.acc_no
                    where lai.acc_no = {accountNo}
                      and lai.account_type = 21
                   """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    yh_count = 2147483647;
    whileFlag = True
    while (whileFlag):

        col_list_js, row_list_js = execute_sql(sql_js, "查询结算账户", db_info[1], db_info[2])
        if row_list_js == None or len(row_list_js) == 0:
            print("结算账户为空！")
            break;

        for index, item in enumerate(row_list_js):

            js_acc_no = item[0]

            col_list_diff, row_list_diff = execute_sql(
                diff_sql_js.format(accNo="'" + js_acc_no + "'", accountNo="'" + js_acc_no + "'"), "查询结算差异", db_info[1],
                db_info[2])

            if row_list_diff != None and len(row_list_diff) != 0:
                js_diff = row_list_diff[0]
                print(js_diff)
                amount = js_diff[1]
                if amount != 0:
                    print("error")

        break
