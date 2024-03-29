import json
import os

import pandas
import pandas as pd

from test.longfor import dbutils
import test.GrantListSql as grant_list_sql
from test.longfor.DBConfig import db_list_info as  db_info_list
from WashGrantOrderSql import check_activity_sql
import WashGrantOrderSql as sql

print_rersult_list = []

# 打印到文件
def writeToExcel(result,sheet_name):
    file_name = "/Users/admin/Desktop/订单模块排查/活动维度排查结果_2022_12_29.xlsx"

    df = pd.DataFrame(result)
    if not os.path.exists(file_name):
        # 写入数据
        with pandas.ExcelWriter(file_name) as write:
            df.to_excel(write, sheet_name, index=False,encoding="utf8")
            write.save()
    else:
        # 写入数据
        with pandas.ExcelWriter(file_name,mode="a") as write:
            df.to_excel(write, sheet_name, index=False, encoding="utf8")
            write.save()

# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/msg_result_12_29.json"
    file = None
    try:
        # if not os.path.exists(path):
        file = open(path, mode="a", encoding="utf-8")
        file.write(msg + "\n")
    except Exception as e:
        print(e)
    finally:
        if file is not None:
            file.close()

def checkGrantOrder(ff_acc_no, activity_no_list):

    activity_no_sql = "(" + json.dumps(activity_no_list).replace("[","").replace("]","").replace('"',"'") + ")"

    # 预算申请
    activity_no_budget_map = dict()
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.platform_grant_budget_apply_sql.format(activity_no_sql), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("查询预算为空:%s" % str(activity_no_list))
    else:
        for index, item in enumerate(row_list_m):
            activity_no_budget_map[item[0]] = item

    # 判断是否全部为订单发放
    is_grant_flag_map = dict()
    for activity_no in activity_no_list:
        is_grant_flag_map[activity_no] = 0

    # 订单模块流水
    activity_no_sum_map = dict()
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.platform_grant_list_sql.format(activity_no_sql), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("订单模块流水为空:%s" % str(activity_no_list))
    else:
        for index,item in enumerate(row_list_m):
            activity_no_sum_map[str(item[0]).strip()] = item

    # 回充数据
    activity_no_backwash_map = dict()
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.platform_grant_backwash_sql.format(activity_no_sql), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("回充数据为空:%s" % str(activity_no_list))
    else:
        for index, item in enumerate(row_list_m):
            activity_no_backwash_map[item[0]] = item

    # 活动清零数据
    activity_no_clear_map = dict()
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.platform_grant_clear_sql.format(activity_no_sql), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("清零数据为空:%s" % str(activity_no_list))
    else:
        for index, item in enumerate(row_list_m):
            activity_no_clear_map[item[0]] = item

    for activity_no in activity_no_list:

        # 初始化数据
        applyAmount = doneGrantSumBd = failGrantSumBd = frozenGrantSum = backwashAndBackinAmount = refundedAmountSum = unRegistExpireSum = availableGrantSum = clearedAmt = 0.0

        #活动预算
        if activity_no_budget_map.__contains__(activity_no):
            applyAmount = activity_no_budget_map[activity_no][1]

        #发放汇总
        if activity_no_sum_map.__contains__(activity_no):
            doneGrantSumBd = activity_no_sum_map[activity_no][2]
            failGrantSumBd = activity_no_sum_map[activity_no][3]
            frozenGrantSum = activity_no_sum_map[activity_no][5]
            refundedAmountSum = activity_no_sum_map[activity_no][6]
            unRegistExpireSum = activity_no_sum_map[activity_no][7]

        #活动回充
        if activity_no_backwash_map.__contains__(activity_no):
            backwashAndBackinAmount = activity_no_backwash_map[activity_no][1]

        #活动清零
        if activity_no_clear_map.__contains__(activity_no):
            clearedAmt = activity_no_clear_map[activity_no][1]

        availableGrantSum = applyAmount - doneGrantSumBd - frozenGrantSum - backwashAndBackinAmount - clearedAmt + refundedAmountSum

        if availableGrantSum == 0.0 or availableGrantSum == -0.0:
            status = "吻合"
        else:
            status = "不符"

        ff_acc_no_list.append(ff_acc_no)
        activity_nos.append(activity_no)
        is_grant_flag_list.append(is_grant_flag_map[activity_no])
        grant_method_name_list.append("-")
        apply_amount_list.append(applyAmount)
        transation_sum_bd_list.append("-")
        done_grant_sum_bd_list.append(doneGrantSumBd)
        refunded_amount_sum_list.append(refundedAmountSum)
        fail_grant_sum_Bbd_list.append(failGrantSumBd)
        frozen_grant_sum_list.append(frozenGrantSum)
        backwash_andBackin_amount_list.append(backwashAndBackinAmount)
        cleared_Amt_list.append(clearedAmt)
        unRegist_expire_sum_list.append(unRegistExpireSum)
        available_grantSum_list.append(availableGrantSum)
        status_list.append(status)

        if availableGrantSum == 0 or availableGrantSum == -0.0:
            print("活动编号:%s,申请金额:%.1f,已发金额:%.1f,发放撤回:%.1f,发放失败:%.1f,未注册待发放:%.1f,已回冲|回冲中金额:%.1f,销账金额:%.1f,未注册待发放-过期:%.1f,待发放金额:%.1f,吻合" % (activity_no, applyAmount, doneGrantSumBd, refundedAmountSum, failGrantSumBd, frozenGrantSum,backwashAndBackinAmount, clearedAmt,unRegistExpireSum,availableGrantSum))
        else:
            print("活动编号:%s,申请金额:%.1f,已发金额:%.1f,发放撤回:%.1f,发放失败:%.1f,未注册待发放:%.1f,已回冲|回冲中金额:%.1f,销账金额:%.1f,未注册待发放-过期:%.1f,待发放金额:%.1f,不符" % (activity_no, applyAmount, doneGrantSumBd, refundedAmountSum, failGrantSumBd, frozenGrantSum,backwashAndBackinAmount, clearedAmt, unRegistExpireSum,availableGrantSum))

    #发放账户清零
    ff_clear = 0.0
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.account_ff_clear_transaction_sql.format("'" + ff_acc_no + "'"), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("发放账户清零数据为空:%s" % str(ff_acc_no))
    else:
        for index, item in enumerate(row_list_m):
            ff_clear = item[1]

    # 发放账户余额｜冻结
    ff_balance = 0.0
    ff_freeze_amount = 0.0
    col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.account_ff_balance_freeze_sql.format("'" + ff_acc_no + "'"), "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("发放账户余额｜冻结数据为空:%s" % str(ff_acc_no))
    else:
        for index, item in enumerate(row_list_m):
            ff_balance = item[1]
            ff_freeze_amount = item[2]

    ff_acc_no_list.append(ff_acc_no)
    activity_nos.append("-")
    is_grant_flag_list.append("-")
    grant_method_name_list.append("-")
    apply_amount_list.append("-")
    transation_sum_bd_list.append("-")
    done_grant_sum_bd_list.append("-")
    refunded_amount_sum_list.append("-")
    fail_grant_sum_Bbd_list.append("-")
    frozen_grant_sum_list.append(ff_freeze_amount)
    backwash_andBackin_amount_list.append("-")
    cleared_Amt_list.append(ff_clear)
    unRegist_expire_sum_list.append("-")
    available_grantSum_list.append(ff_balance)
    status_list.append("-")

def checkActivity(ff_acc_no, activity_no):
    col_list_m, row_list_g = dbutils.execute_sql(check_activity_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'", "'" + getExtra(activity_no) + "'"), "确认是否合格")
    if row_list_g is not None and len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,查询确认结果为空" % (ff_acc_no, activity_no))
        raise TypeError
    else:
        check_flag = False
        if row_list_g[0] is not None and row_list_g[0][0] is not None and row_list_g[0][1] is not None:
            if row_list_g[0][0] == row_list_g[0][1]:
                check_flag = True

        if check_flag:
            print("发放账户,ff_acc_no = %s,activity_no = %s,订单模块净发放:%s,项目公司流水净发放:%s,已确认,符合" % (ff_acc_no, activity_no,str(row_list_g[0][0]),str(row_list_g[0][1])))
        else:
            print("发放账户,ff_acc_no = %s,activity_no = %s,订单模块净发放:%s,项目公司流水净发放:%s,已确认,不符合" % (ff_acc_no, activity_no,str(row_list_g[0][0]),str(row_list_g[0][1])))

"""
获取扩展字段
"""
def getExtra(activity_no):
    return '{"activity_no":"%s","source":"platform_grant"}' % activity_no


if __name__ == "__main__":

    db_info = db_info_list[0]

    ff_acc_no = "FF-200727-01740"

    ff_acc_no_map = dict()
    col_list_m, row_list_g = dbutils.execute_sql(sql.select_budget_appply_ff_acc_no_sql.format("'" + ff_acc_no + "'"), "查询活动")
    if row_list_g is None and len(row_list_g) <= 0:
        raise TypeError
    else:
        for item in row_list_g:
            activity_no = item[1]
            if ff_acc_no_map.__contains__(ff_acc_no):
                ff_acc_no_map[ff_acc_no].append(activity_no)
            else:
                ff_acc_no_map[ff_acc_no] = [activity_no]

    # 待发放金额 = 申请金额 - 已发金额 - 未注册待发放 - 已回冲金额 - 回冲中 - 销账金额
    result_map = dict()
    ff_acc_no_list = []
    activity_nos = []
    is_grant_flag_list = []
    grant_method_name_list = []
    apply_amount_list = []
    transation_sum_bd_list = []
    done_grant_sum_bd_list = []
    fail_grant_sum_Bbd_list = []
    frozen_grant_sum_list = []
    backwash_andBackin_amount_list = []
    refunded_amount_sum_list = []
    unRegist_expire_sum_list = []
    available_grantSum_list = []
    cleared_Amt_list = []
    status_list = []


    # for ff_acc_no,activity_no_list in ff_acc_no_map.items():
    #     if activity_no_list is not None and len(activity_no_list) > 0:
    #         for activity_no in activity_no_list:
    #             checkActivity(ff_acc_no, activity_no)
    ff_acc_no_map = dict()
    ff_acc_no_map['FF-210910-27129'] = ['YH2301031519CJ58701']

    index_flag = 0
    for ff_acc_no,activity_no_list in ff_acc_no_map.items():
        index_flag+=1
        print("当前条数:%d" % index_flag)
        print("发放账户:%s,开始" % ff_acc_no)
        ## 核心查询逻辑
        checkGrantOrder(ff_acc_no,activity_no_list)
        print("发放账户:%s,结束" % ff_acc_no)


    result_map["发放账户"] = ff_acc_no_list
    result_map["活动编号"] = activity_nos
    result_map["申请金额"] = apply_amount_list
    result_map["是否订单发放"] = is_grant_flag_list
    result_map["发放方式"] = grant_method_name_list
    result_map["流水已发金额"] = transation_sum_bd_list
    result_map["已发金额"] = done_grant_sum_bd_list
    result_map["发放撤回"] = refunded_amount_sum_list
    result_map["发放失败"] = fail_grant_sum_Bbd_list
    result_map["未注册待发放"] = frozen_grant_sum_list
    result_map["已回冲|回冲中金额"] = backwash_andBackin_amount_list
    result_map["销账金额"] = cleared_Amt_list
    result_map["未注册待发放-过期"] = unRegist_expire_sum_list
    result_map["待发放金额"] = available_grantSum_list
    result_map["状态"] = status_list

    writeToExcel(result_map,ff_acc_no)

