from DBConfig import db_list_info as  db_info_list
import dbutils
import json
import requests
from GrantOrderFFAccount import except_acc_no_list as except_acc_no_list
from GrantOrderFFAccount import not_check_list as not_check_list
from decimal import Decimal

server = "http://127.0.0.1:8066/queryOrderNo"


def post_lmarketing(params):
    data = {
        "list": params
    }
    head = {
        "Content-Type": "application/json"
    }

    return invoke_post(server, head, data)


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=json.dumps(params), timeout=1000, headers=head)
    if resp.text is not None and resp.text != '[]':
        print("大会员活动流水,活动编号票响应:{%s}" % resp.text)
    return resp.text


def checkFromLmarketing(trans_no_list):
    # 查询大会员
    lmarketing = post_lmarketing(trans_no_list)
    if lmarketing is not None and len(lmarketing) > 0:
        if len(lmarketing) != len(trans_no_list):
            print("查询流水号:%.1f,结果流水号:%.1f" % (len(trans_no_list), len(lmarketing),))
            # TODO
        for itsm in lmarketing:
            order_no = itsm["orderNo"]
            if order_no not in trans_no_list:
                print()
            print()
    trans_no_list.clear()

# 打印到文件
# def print(result,flag = False,boo = False):
#
#     if boo:
#         print(result)
#
#     print_rersult_list.append(result + "\n")
#     if len(print_rersult_list) % 100 == 0:
#         file_result = open("/Users/admin/Desktop/订单模块排查/ff_acc_no_result.json", mode="a+", encoding="utf-8")
#         file_result.writelines(print_rersult_list)
#         file_result.flush()
#         file_result.close()
#
#         print_rersult_list.clear()
#     if flag:
#         file_result = open("/Users/admin/Desktop/订单模块排查/ff_acc_no_result.json", mode="a+", encoding="utf-8")
#         file_result.writelines(print_rersult_list)
#         file_result.flush()
#         file_result.close()
#
#         print_rersult_list.clear()


def checkGrantOrder(db_info, ff_acc_no):
    # 发放｜撤回
    ff_company_transaction_sql = """
                select acc_no,out_trans_no,target_acc_no,trans_amt,extra,trans_type from t_company_transaction where acc_no = {2} and target_acc_no regexp 'XF|YH|SH|GLZ' and `status` = 1 order by id limit {0},{1};
            """

    # 充值｜活动回充｜冻结｜解冻
    cz_company_transaction_sql = """
                    select acc_no,out_trans_no,target_acc_no,trans_amt,trans_type,serial_number,purpose from t_company_transaction where acc_no = {0} and target_acc_no not regexp 'XF|YH|SH|GLZ' and `status` = 1 order by trans_type;
                """

    platform_grant_budget_apply_sql = """
                    select apply_amount,recharge_status,fk_preuse_id from t_platform_grant_budget_apply where activity_no = {0};
                """

    platform_grant_list_sql = """
                        select count(*) from t_platform_grant_list where activity_no = {0} and grant_status = 1 and is_deleted = 0;
                    """

    platform_grant_sum_sql = """
                        select sum(grant_amount) from t_platform_grant_list where activity_no = {0} and grant_status = 1 and is_deleted = 0;
                    """

    lfm_account_balance_sql = """
             SELECT lai.acc_no,lab.balance,lab.freeze_amount
                FROM lfm_account_info as lai, lfm_account_balance as lab
                WHERE lai.account_type = 20 and lai.account_id=lab.account_id and lai.acc_no = {0};
         """

    grant_sum_sql = """
            select sum(if(trans_type = 2,trans_amt,-trans_amt)) from t_company_transaction where acc_no = {0} and target_acc_no regexp 'XF|YH|SH|GLZ' and `status` = 1;
        """

    start_id = 0
    page_limit = 10000
    activity_no_map = dict()
    activity_no_sum_map = dict()
    # 初始化非活动发放金额
    activity_no_sum_map[ff_acc_no] = Decimal("0")
    while True:
        # 查询流水
        col_list_m, row_list_m = dbutils.execute_sql(ff_company_transaction_sql.format(start_id, page_limit, "'" + ff_acc_no + "'"), "查询流水", db_info[1],db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            break
        else:
            start_id += page_limit

            trans_no_list = []
            for idex, itsm in enumerate(row_list_m):
                trans_no_list.append(itsm[1])
                amt = int(itsm[3] * 100)


                # 活动发放
                if itsm[4] is not None and itsm[4] != '':
                    extra = ""
                    try:
                        extra = json.loads(itsm[4])
                        activity_no = extra["activity_no"]
                        if activity_no == "null":
                            if itsm[5] == 1:
                                activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] - Decimal(amt)
                            elif itsm[5] == 2:
                                activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] + Decimal(amt)
                            else:
                                print("发放流水错误,交易发放为空,out_trans_no:%s" % itsm[1])
                            continue
                    except:
                        # print("activity_no:%s,格式转化异常" % itsm[4])
                        # raise TypeError("格式转化异常")
                        # 活动编号格式错误，计入发放账户金额

                        # trans_type = 2,发放，trans_type = 1撤回
                        if itsm[5] == 1:
                            activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] - Decimal(amt)
                        elif itsm[5] == 2:
                            activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] + Decimal(amt)
                        else:
                            print("发放流水错误,交易发放为空,out_trans_no:%s" % itsm[1])
                        continue

                    if activity_no_map.__contains__(activity_no):
                        activity_no_list = activity_no_map[activity_no]
                        if isinstance(activity_no_list, list):
                            activity_no_list.append(itsm[1])
                        else:
                            activity_no_map[activity_no] = [activity_no_list, itsm[1]]

                        # trans_type = 2,发放，trans_type = 1撤回
                        if itsm[5] == 1:
                            activity_no_sum_map[activity_no] = activity_no_sum_map[activity_no] - Decimal(amt)
                        elif itsm[5] == 2:
                            activity_no_sum_map[activity_no] = activity_no_sum_map[activity_no] + Decimal(amt)
                        else:
                            print("发放流水错误,交易发放为空,out_trans_no:%s" % itsm[1])
                    else:
                        activity_no_map[activity_no] = [itsm[1]]
                        activity_no_sum_map[activity_no] = Decimal(amt)
                else:
                    # 非活动发放
                    # trans_type = 2,发放，trans_type = 1撤回
                    if itsm[5] == 1:
                        activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] - Decimal(amt)
                    elif itsm[5] == 2:
                        activity_no_sum_map[ff_acc_no] = activity_no_sum_map[ff_acc_no] + Decimal(amt)
                    else:
                        print("发放流水错误,交易发放为空,out_trans_no:%s" % itsm[1])

            #     if len(trans_no_list) == 1000:
            #         checkFromLmarketing(trans_no_list)
            # if len(trans_no_list) > 0:
            #     checkFromLmarketing(trans_no_list)


    # 校验预算申请
    budget_amount = 0
    for activity_no in activity_no_map.keys():
        col_list_m, row_list_m = dbutils.execute_sql(platform_grant_budget_apply_sql.format("'" + activity_no + "'"),"查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            print("activity_no:%s,查询预算为空" % activity_no)
        else:
            # 校验grant_list汇总总额
            col_list, row_list = dbutils.execute_sql(platform_grant_sum_sql.format("'" + activity_no + "'"),"查询流水", db_info[1], db_info[2])

            if row_list is None or len(row_list) == 0:
                print("activity_no:%s,查询grant_list汇总总额为空" % activity_no)
            else:
                grant_sum = row_list[0][0]

            row = row_list_m[0]
            budget_amount = budget_amount + row[0]
            # if row[1] is None or row[1] != 1:
            #     print("activity_no:%s,预算充值状态未记录" % activity_no)

            no_ = activity_no_sum_map[activity_no] / 100
            if grant_sum != row[0]:
                print("activity_no:%s,apply_amount:%.1f,grant_amount:%.1f,grant_sum:%.1f,fk_preuse_id:%s,预算和发放总额不符" % (activity_no, row[0], no_,grant_sum, row[2]))
            else:
                print("activity_no:%s,apply_amount:%.1f,grant_amount:%.1f,grant_sum:%.1f,fk_preuse_id:%s,预算和发放总额吻合" % (activity_no, row[0], no_,grant_sum, row[2]))

    # 校验grant_list
    for activity_no in activity_no_map.keys():
        col_list_m, row_list_m = dbutils.execute_sql(platform_grant_list_sql.format("'" + activity_no + "'"), "查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            print("activity_no:%s,发放集合为空" % activity_no)
        else:
            row = row_list_m[0]
            if len(activity_no_map[activity_no]) == row[0]:
                print("activity_no:%s,发放流水数量:%.1f,grant_list数量:%.1f 吻合" % (
                    activity_no, len(activity_no_map[activity_no]), row[0]))
            else:
                print("activity_no:%s,发放流水数量:%.1f,grant_list数量:%.1f 不符" % (
                    activity_no, len(activity_no_map[activity_no]), row[0]))

    # 校验充值｜活动回充｜冻结｜解冻|销账
    cz_amount = 0.0
    hc_amount = 0.0
    dj_amount = 0.0
    jd_amount = 0.0
    nm_amount = 0.0
    xz_amount = 0.0
    col_list_m, row_list_m = dbutils.execute_sql(cz_company_transaction_sql.format("'" + ff_acc_no + "'"), "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        print("发放账户:%s,发放账户充值｜活动回充｜冻结｜解冻为空" % ff_acc_no)
    else:
        for index, item in enumerate(row_list_m):
            trans_type = item[4]
            amount = float(item[3])
            if trans_type == 1:
                print("充值流水:out_trans_no:%s,serial_number:%s,trans_amt:%.1f" % (item[1], item[5], amount))
                cz_amount = cz_amount + amount
            elif trans_type == 5:
                dj_amount = dj_amount + amount
            elif trans_type == 6:
                jd_amount = jd_amount + amount
            elif trans_type == 7:
                hc_amount = hc_amount + amount
            else:
                if item[6] == "发放撤回-发放账户销账" and item[4] == 2:
                    xz_amount = xz_amount + amount
                elif item[6] == "定时任务-年末余额收回":
                    nm_amount = nm_amount + amount
                else:
                    print("非发放流水,异常数据:%s" % item)



    # 校验账户余额,冻结金额
    balance = 0.0
    freeze_amount = 0.0
    col_list_m, row_list_m = dbutils.execute_sql(lfm_account_balance_sql.format("'" + ff_acc_no + "'"), "查询流水",
                                                 db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        print("activity_no:%s,发放账户为空" % ff_acc_no)
    else:
        balance = row_list_m[0][1]
        freeze_amount = row_list_m[0][2]

    # 发放总额
    grant_total = Decimal("0")
    for amt in activity_no_sum_map.values():
        # TODO
        grant_total = grant_total + amt

    grant_total = float(grant_total)/100

    # 发放汇总数据
    col_list_m, row_list_m = dbutils.execute_sql(grant_sum_sql.format("'" + ff_acc_no + "'"), "查询流水",
                                                 db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        print("发放账户：%s，查询总发放聚合为空" % ff_acc_no)
    else:
        if grant_total != row_list_m[0][0]:
            print("发放汇总数据不一致：发放汇总:%.1f，聚合查询:%.1f不符" % (grant_total, row_list_m[0][0]))
            grant_total = row_list_m[0][0]


    # 差异比较
    if budget_amount != cz_amount:
        print("发放账户:%s,预算:%.1f,充值:%.1f,不符" % (ff_acc_no, budget_amount, cz_amount))
    else:
        print("发放账户:%s,预算:%.1f,充值:%.1f,吻合" % (ff_acc_no, budget_amount, cz_amount))

    if dj_amount - jd_amount - hc_amount - freeze_amount != 0:
        print("发放账户:%s,冻结:%.1f,解冻:%.1f,活动回充:%.1f,账户冻结:%.1f,冻结-解冻-活动回充-账户冻结,结果不符" % (
            ff_acc_no, dj_amount, jd_amount, hc_amount, freeze_amount))
    else:
        print("发放账户:%s,冻结:%.1f,解冻:%.1f,活动回充:%.1f,账户冻结:%.1f,冻结-解冻-活动回充-账户冻结,结果吻合" % (
            ff_acc_no, dj_amount, jd_amount, hc_amount, freeze_amount))

    result_diff = cz_amount - grant_total - balance - hc_amount - nm_amount - xz_amount
    if result_diff != 0:
        print("发放账户:%s,充值:%.1f,发放:%.1f,余额:%.1f,账户冻结:%.1f,活动回充:%.1f,发放账户年末收回:%.1f,发放销账:%.1f,差额:%.1f,充值-发放-余额-活动回充,结果不符" % (
            ff_acc_no, cz_amount, grant_total, balance, freeze_amount, hc_amount, nm_amount, xz_amount, result_diff))
    else:
        print("发放账户:%s,充值:%.1f,发放:%.1f,余额:%.1f,账户冻结:%.1f,活动回充:%.1f,发放账户年末收回:%.1f,发放销账:%.1f,差额:%.1f,充值-发放-余额-活动回充,结果吻合" % (
            ff_acc_no, cz_amount, grant_total, balance, freeze_amount, hc_amount, nm_amount, xz_amount, result_diff))

    # 汇总数据
    print("汇总数据,发放账户:%s,充值:%.1f,活动回充:%.1f,冻结:%.1f,解冻:%.1f,发放:%.1f,余额:%.1f,账户冻结:%.1f" % (
        ff_acc_no, cz_amount, hc_amount, dj_amount, jd_amount, grant_total, balance, freeze_amount))


def queryGrantOrderByFFAccNo(acc_no_list,sql):
    # 查询发放账户的问题
    try:
        col_list_m, row_list_m = dbutils.execute_sql(sql.format("(" + json.dumps(acc_no_list).replace("[", "").replace("]", "") + ")"),"查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            pass
        else:
            for item in row_list_m:
                print("发放账户：%s,活动详情：%s" % (item[0], item[1]))
    except Exception as e:
        print(e)
    finally:
        acc_no_list.clear()

"""查询所有涉及订单模块账户"""
def queryOrderFFAccNo():
    ff_acc_no_sql = """
            select acc_no from lfm_account_info where account_type = 20 order by account_id limit {0},{1}
        """

    incloud_grant_order_acc_no_sql = """
                select acc_no,extra from t_company_transaction where acc_no in {0} and target_acc_no regexp 'XF|YH|SH' and extra is not null and extra != '' group by acc_no,extra;
            """

    page_size = 1000
    page_start = 3700

    while True:
        col_list_m, row_list_m = dbutils.execute_sql(ff_acc_no_sql.format(page_start, page_size), "查询流水", db_info[1],
                                                     db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            break
        else:
            page_start = page_start + page_size
            acc_no_list = []
            for acc_no in row_list_m:
                # print("发放账户：%s" % acc_no)
                if acc_no[0] == 'FF-210305-05605':
                    print("发放账户：FF-210305-05605")
                    continue
                acc_no_list.append(acc_no[0])
                if len(acc_no_list) % 100 == 0:
                    queryGrantOrderByFFAccNo(acc_no_list,incloud_grant_order_acc_no_sql)

            # 最后一页账户
            if len(acc_no_list) % 100 > 0 and len(acc_no_list) < 100:
                queryGrantOrderByFFAccNo(acc_no_list,incloud_grant_order_acc_no_sql)


print_rersult_list = []

if __name__ == "__main__":

    db_info = db_info_list[0]


    #1、查询所有涉及订单模块账户
    # queryOrderFFAccNo()

    # file = open("/Users/admin/Desktop/订单模块排查/ff_acc_no_list.json", mode="r", encoding="utf-8")
    # ff_acc_no_list = []
    # for acc_no in file.readlines():
    #     ff_acc_no_list.append(str(acc_no))
    #
    # ff_acc_no_list.sort()

    #2、 查询每个账户的详情数据
    # for acc_no in ff_acc_no_list:
    #
    #     acc_no = acc_no.replace("\n","")
    #
    #     # 排出已出现结果的账户
    #     if acc_no in except_acc_no_list:
    #         continue
    #
    #     print("发放账户:%s,开始" % acc_no)
    #     checkGrantOrder(db_info,acc_no)
    #     print("发放账户:%s,结束\n" % acc_no,True)
    #3、特殊账户处理
    for acc_no in not_check_list:
        print("发放账户:%s,开始" % acc_no)
        checkGrantOrder(db_info,acc_no)
        print("发放账户:%s,结束\n" % acc_no)