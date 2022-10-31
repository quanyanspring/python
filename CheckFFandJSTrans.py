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
        "Cookie": "CASTGC=TGT-1340816-g4hHIa9ngEuUqjmKoU9HrwYTx0en1Nqka8Cm0u36sgp9k8VAc7Y6JUQ1WLQ6YRu2O3E-longhu; account=TGT-1340816-g4hHIa9ngEuUqjmKoU9HrwYTx0en1Nqka8Cm0u36sgp9k8VAc7Y6JUQ1WLQ6YRu2O3E-longhu; sessionid=lkz6ix4wfbw8mjhcbqjo1blbe7xsuvxr",
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
        "limit_num": 100
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
    # print(a)
    a = a + 1
    return a


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    yh_sql = """
        select order_no, trans_amount from lfm_account_log where account_type = '20' and other_account_type = '2'order by create_time asc limit {0}, 100;
    """

    ff_sql = """
        select order_no,trans_amount from lf_account_log where order_no = {0} and account_type = 2 and other_account_type = 20;
    """

    # lfm_account_log > lf_account_log
    diff_sql_b = """
        select lm.order_no,lm.trans_amount from (select * from lfm_account_log where  create_time >={0} and create_time < {1} and account_type = '20' and other_account_type = '2') lm left join (
            select * from lf_account_log where  create_time >={2} and create_time < {3} and acc_no like 'YH%' and (other_acc_no regexp 'FF|QYFF') = 1) l on lm.order_no = l.order_no where l.order_no is null;
    """

    # lfm_account_log < lf_account_log
    diff_sql_c = """
        select l.order_no, l.trans_amount from (select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = '20' and other_account_type = '2') lm right join (
            select * from lf_account_log where create_time >={2} and create_time < {3} and acc_no like 'YH%' and (other_acc_no regexp 'FF|QYFF') = 1) l on lm.order_no = l.order_no where lm.order_no is null;
    """

    # lfm_account_log < t_activity_result_log
    diff_sql_l = """
        select tarl.trans_no from (
            select * from lfm_account_log where create_time >={0} and create_time <{1} and account_type = 20) lfm
            right join (
            select * from t_activity_result_log where create_time >={2} and create_time <{3} and code <> '40074' and status = 1
            ) tarl on lfm.order_no = tarl.trans_no where lfm.id is null
    """

    # lfm_account_log > t_activity_result_log
    diff_sql_m = """
        select t.* from (
        select lfm.order_no from (
                select * from lfm_account_log where create_time >={0} and create_time <{1} and account_type = 20 and other_account_type <> 21 and business_type <> '40074' and trans_amount > 0 and remark not in (
                '权益发放充值','膨胀金发放充值','hrπ珑珠充值','老带新珑珠充值','业主赔付珑珠充值','C1运营赔付珑珠充值') and order_no not like 'M%') lfm left join (select * from t_activity_result_log where create_time >={2} and create_time <{3} order by create_time asc) tarl on lfm.order_no = tarl.trans_no where tarl.trans_no is null) t limit {4},100;
    """

    #lf_account_log > t_activity_result_log(count)
    diff_sql_m_count = """
        select count(1) from (
                select * from lfm_account_log where create_time >={0} and create_time <{1} and account_type = 20 and other_account_type <> 21 and business_type <> '40074' and trans_amount > 0 and remark not in (
                '权益发放充值','膨胀金发放充值','hrπ珑珠充值','老带新珑珠充值','业主赔付珑珠充值','C1运营赔付珑珠充值','老带新充值') and order_no not like 'M%') lfm left join (select * from t_activity_result_log where create_time >={2} and create_time <{3}) tarl on lfm.order_no = tarl.trans_no where tarl.trans_no is null;
    """

    #t_activity_result_log > t_grant_budget_prehandle
    diff_sql_r = """
        select * from (
        select tarl.trans_no from (
            select * from t_activity_result_log where create_time >= {0} and create_time < {1} and biz_sys_id in ('121','113')) tarl left join (
            select * from t_grant_budget_prehandle where create_time >= {2} and create_time < {3}
            ) tg on tarl.trans_no = tg.trans_no where tg.trans_no is null) t limit {4}, 100;
    """

    #t_activity_result_log > t_grant_budget_prehandle(count)
    diff_sql_r_count = """
        select count(1) from (
        select tarl.trans_no from (
            select * from t_activity_result_log where create_time >= {0} and create_time < {1} and biz_sys_id in ('121','113')) tarl left join (
            select * from t_grant_budget_prehandle where create_time >= {2} and create_time < {3}
            ) tg on tarl.trans_no = tg.trans_no where tg.trans_no is null) t;
    """

    #t_activity_result_log > t_grant_budget_prehandle
    diff_sql_p = """
        select * from (
        select tg.trans_no from (
            select * from t_activity_result_log where create_time >= {0} and create_time < {1}) tarl right join (
            select * from t_grant_budget_prehandle where create_time >= {2} and create_time < {3}
            ) tg on tarl.trans_no = tg.trans_no where tarl.trans_no is null) t limit {4}, 100;
    """

    #t_activity_result_log > t_grant_budget_prehandle(count)
    diff_sql_p_count = """
        select count(1) from (
        select tg.trans_no from (
            select * from t_activity_result_log where create_time >= {0} and create_time < {1}) tarl right join (
            select * from t_grant_budget_prehandle where create_time >= {2} and create_time < {3}
            ) tg on tarl.trans_no = tg.trans_no where tarl.trans_no is null) t;
    """

    # t_activity_result_log > t_grant_budget_prehandle
    diff_sql_j = """
            select t.* from (
            select tarl.order_no from (
                select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = 20 and other_account_type != 25 ) tarl left join 
                ( select * from lfm_account_log where create_time >= {2} and create_time < {3} and account_type = 21 and other_account_type = 20
                ) tg on tarl.order_no = tg.order_no where tg.order_no is null) t;
        """

    # t_activity_result_log > t_grant_budget_prehandle(count)
    diff_sql_j_count = """
            select count(1) from (
            select tarl.order_no from (
                select order_no from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = 20 and other_account_type != 25 ) tarl left join 
                ( select order_no from lfm_account_log where create_time >= {2} and create_time < {3} and account_type = 21 and other_account_type = 20 ) tg on tarl.order_no = tg.order_no 
                where tg.order_no is null) t;
        """

    diff_sql_js = """
                select count(1) from (
                select tarl.order_no from (
                    select order_no from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = 20 and other_account_type != 25 ) tarl left join 
                    ( select order_no from lfm_account_log where create_time >= {2} and create_time < {3} and account_type = 21 and other_account_type = 20 ) tg on tarl.order_no = tg.order_no 
                    where tg.order_no is null) t;
            """

    diff_sql_js_count = """
                select count(1) from (
                select tarl.order_no from (
                    select order_no from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = 20 and other_account_type != 25 ) tarl left join 
                    ( select order_no from lfm_account_log where create_time >= {2} and create_time < {3} and account_type = 21 and other_account_type = 20 ) tg on tarl.order_no = tg.order_no 
                    where tg.order_no is null) t;
            """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    total = 0
    yh_count = 2147483647;

    # e = datetime.datetime.strptime('2022-01-10 00:00:00', '%Y-%m-%d %H:%M:%S')
    # d = datetime.datetime.strptime('2021-06-24 00:00:00', '%Y-%m-%d %H:%M:%S')
    e = datetime.datetime.strptime('2022-12-08 00:00:00', '%Y-%m-%d %H:%M:%S')
    d = datetime.datetime.strptime('2021-12-07 00:00:00', '%Y-%m-%d %H:%M:%S')
    l = d
    for i in range(yh_count):
        d = l
        l = d + datetime.timedelta(days=1)

        print("==>当前日期为:" + d.strftime('%Y-%m-%d %H:%M:%S'))
        # print("==>当前日期为:" + l.strftime('%Y-%m-%d %H:%M:%S'))
        if e - d <= datetime.timedelta(days=0):
            break

        diff_sql_j_count = diff_sql_j_count.format("'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                    "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                    "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                    "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'")

        col_list_m, row_list_m = execute_sql(diff_sql_j_count, "查询用户流水", db_info[1], db_info[2])
        if row_list_m == None or len(row_list_m) == 0:
            continue

        count = row_list_m[0][0]
        if count == 0:
            continue

        cicle = 1
        if count > 100:
            if count % 100 == 0:
                cicle = count // 100
            else:
                cicle = count // 100 + 1

        for i in range(0, cicle):
            diff_sql1 = diff_sql_j.format("'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                          "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                          "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                          "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                          100 * i)
            # yh_sql_page = yh_sql.format(i * 100)
            col_list, row_list = execute_sql(diff_sql1, "查询用户流水", db_info[1], db_info[2])
            if row_list == None or len(row_list) == 0:
                continue

            # 标题列
            # if get_count() == 1:
            #     print("写入标题列")
            #     # worksheet.write(0, 0, "外部发放C端多")
            #     for i in range(0, len(col_list)):
            #         col_str = col_list[i]
            #         worksheet.write(0, i, col_str)

            for j in range(len(row_list)):
                row = row_list[j]
                # worksheet.write(0, i, row[0])
                print(row[0])

    # print("==>总共处理记录" + str(total) + "条记录")
    # 保存文件
    workbook.save('/Users/admin/Desktop/大等式/外部用户发放流水对账_B端.xlsx')
