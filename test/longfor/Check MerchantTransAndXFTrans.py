import requests
import json
from prettytable import PrettyTable
import datetime
import time
import xlwt
import DBConfig as config

server = "http://dbaexecsql.longfor.com/data_application/app_query/"
global a, b, c
a = ""
b = 0
c = 0


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
def execute(sql, detail, instance, db_name, limit):
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
        "limit_num": limit
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
        # full_sql = data_cont["full_sql"]
        # error = data_cont["error"]
        query_time = data_cont["query_time"]
        print("查询时间：{0}sec".format(query_time))

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


# 全局计数器 - 账户分页id
def get_acc_no_count():
    global a
    print(a)
    return a


# 全局计数器 - 账户分页id
def set_acc_no_count(acc_no):
    global a
    a = acc_no
    print("设置账户分页= {0}".format(a))


# 全局计数器 - 文件写入
def get_sheet_count():
    global c
    print(c)
    return c


# 全局计数器
def set_sheet_count(num=1):
    global c
    c = c + num
    print("设置问题表id= {0}".format(b))


# 全局计数器 - 流水分页id
def get_count():
    global b
    print(b)
    return b


# 全局计数器 - 流水分页id
def set_count(id):
    global b
    b = id
    print("设置分页id= {0}".format(b))


if __name__ == "__main__":

    # 数据库配置信息
    db_info = config.db_list_info[0]

    # 账户循环sql
    mer_account_sql = """
        select * from lfm_account_info where account_type = 22 and acc_no = {accountNo} order by acc_no;
        """

    # xf_account_no = "XF-210407-55714"

    # 商户流水sql
    merchant_trans_sql = """
                select * from t_merchant_transaction where acc_no = {accNo} and status = 1 and id > {id} and devide_type = 0 order by id ;
                """

    # 账户流水sql
    xf_trans_sql = """
        select * from lf_account_log where order_no in {orderNoList} and other_acc_no = {otherAccNo} and other_account_type in (0,22) ;
        """

    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    account_flag = True
    account_count = 0
    while account_flag:
        account_count += 1

        account_no = get_acc_no_count()
        if account_count == 1:
            account_no = "SH-200707-000132"

        # 查询账户信息
        col_list, account_info_list = execute_sql(mer_account_sql.format(accountNo="'" + account_no + "'"), "查询账户",
                                                  db_info[1],
                                                  db_info[2], 1000)
        if account_info_list == None and len(account_info_list) == 0:
            break
        if len(account_info_list) < 1000:
            account_flag = False

        # 标题列
        col = ()
        if get_sheet_count() == 0:
            print("写入标题列")
            worksheet.write(0, 0, "商户")
            worksheet.write(0, 1, "sum_balance")
            worksheet.write(0, 2, "sum_balance")
            worksheet.write(0, 3, "sum_balance")
            set_sheet_count()

        # 循环账号
        for index, row in enumerate(account_info_list):
            acc_no = row[1]

            if index + 1 == len(account_info_list):
                set_acc_no_count(acc_no)

            # 获取内部账户流水-分页查询
            none = True
            count = 0
            while none:
                count += 1

                # 查询商户流水
                xf_col_list, mer_trans_list = execute_sql(
                    merchant_trans_sql.format(accNo="'" + acc_no + "'", id=get_count()),
                    "查询内部账户流水",
                    db_info[1], db_info[2], 1000)
                if mer_trans_list == None or len(mer_trans_list) < 1:
                    print("内部账户：{0},流水结果集为空，结束循环".format(acc_no))
                    break
                if len(mer_trans_list) < 100:
                    none = False

                # 构建order_no结果集
                mer_order_no = ""
                temp_order_no_list = []
                # order_no item字典
                order_dict = {}
                for idx, item in enumerate(mer_trans_list):
                    order_no = item[3]
                    trans_amount = item[7]
                    id = item[0]
                    temp_order_no_list.append("'" + str(order_no) + "'")
                    mer_order_no = ",".join(temp_order_no_list)

                    order_dict[order_no] = trans_amount

                    # 设置最大id
                    size = idx + 1
                    if size == len(mer_trans_list):
                        set_count(id)

                mer_order_no = "(" + mer_order_no + ")"

                # 查询用户流水
                mer_col_lis, xf_trans_list = execute_sql(
                    xf_trans_sql.format(orderNoList=mer_order_no, otherAccNo="'" + acc_no + "'"),
                    "查询商户账户流水",
                    db_info[1], db_info[2])

                if xf_trans_list == None or len(xf_trans_list) < 1:
                    print("内部账户：{0},流水为空,orderNo = {1}".format(acc_no, mer_order_no))
                else:
                    print("处理对账流水开始：{0}".format(acc_no))
                    xf_count = len(xf_trans_list)
                    mer_count = len(mer_trans_list)
                    if xf_count != mer_count:
                        xf_order_no = ""
                        xf_order_no_list = []
                        for i in range(len(xf_trans_list)):
                            xf_order_no_list.append("'" + str(xf_trans_list[i][2]) + "'")
                            mer_order_no = ",".join(xf_order_no_list)
                        # 如果当前账户用户流水比商户多，不再对比该账户
                        print("商户账户：{0},用户流水条数：{1},商户流水条数：{2},用户流水：{3},商户流水：{4}".format(acc_no, xf_count, mer_count,
                                                                                        xf_order_no, mer_order_no))
                        dif = list(set(temp_order_no_list) ^ set(xf_order_no_list))
                        str_dif = ",".join(dif)
                        worksheet.write(get_sheet_count(), 0, xf_count)
                        worksheet.write(get_sheet_count(), 1, mer_count)
                        worksheet.write(get_sheet_count(), 2, str_dif)
                        set_sheet_count()

                    for mer_index, mer_row in enumerate(xf_trans_list):
                        out_trans_no = mer_row[2]
                        trans_amt = mer_row[7]

                        if out_trans_no in order_dict.keys():
                            if trans_amt == order_dict[out_trans_no]:
                                print("对账成功")
                            else:
                                print("开始写入错误数据")
                                worksheet.write(get_sheet_count(), 0, out_trans_no)
                                worksheet.write(get_sheet_count(), 1, trans_amt)
                                worksheet.write(get_sheet_count(), 2, out_trans_no)
                                worksheet.write(get_sheet_count(), 3, order_dict[out_trans_no])
                                set_sheet_count()
                        else:
                            print("开始写入错误数据")
                            worksheet.write(get_sheet_count(), 0, out_trans_no)
                            worksheet.write(get_sheet_count(), 1, order_dict[out_trans_no])
                            set_sheet_count()

                print("内部账户：{0},对账循环第：{1},次".format(acc_no, count))

            # 重置id
            set_count(0)
            print("内部账户：{0},对账结束".format(acc_no))

        print("内部所有账户，对账循环第：{},次".format(account_count))

        time.sleep(1)

    # 保存文件
    workbook.save('/Users/admin/Desktop/大等式/商户流水和用户流水比较_1.xls')
