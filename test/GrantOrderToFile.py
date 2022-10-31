from DBConfig import db_list_info as  db_info_list
import pandas as pd
from utils import WriteToExcelUtil as writeUtil
from GrantOrderFFAccount import is_check_out_ff_acc_no_list
import dbutils
import GrantListSql as grant_list_sql

if __name__ == "__main__":

    db_info = db_info_list[0]

    # 读所有活动与发放账户对应关系数据
    excel = pd.read_excel("/Users/admin/Desktop/export_result.xlsx")
    df = excel[["activityNo", "activityStatus", "grantMethod", "applyAmount"]]
    activity_no_map = dict()
    index = 0
    for item in df["activityNo"]:
        activity_no_map[item] = [df["activityStatus"][index], df["grantMethod"][index], df["applyAmount"][index]]
        index += 1

    excel = pd.read_excel("/Users/admin/Desktop/订单模块排查/activityNoAcc.xlsx", sheet_name="Sheet1")

    # 去掉空值的行 nan
    excel.dropna()

    ncols = excel.shape[0]
    activity_no_col = 0
    ff_acc_no_col = 2

    # 去除发放活动为名单发放的发放账户
    ff_acc_list = []
    for iCol in range(ncols):
        activity_no = excel.iloc[iCol, activity_no_col]
        ff_acc_no = excel.iloc[iCol, ff_acc_no_col]

        if str(ff_acc_no) == 'nan':
            continue

        # 排出名单发放
        grant_method = activity_no_map[activity_no][1]
        if not grant_method == 1:
            continue
        else:
            ff_acc_list.append(ff_acc_no)

    ff_acc_list = list(set(ff_acc_list))

    # 活动申请金额
    ff_acc_no_activity_sum = dict()
    # 活动申请数量
    ff_acc_no_activity_num = dict()

    # 涉及上述结果的所有发放账户
    for iCol in range(ncols):
        activity_no = excel.iloc[iCol, activity_no_col]
        ff_acc_no = excel.iloc[iCol, ff_acc_no_col]

        # 过滤特殊情况
        if not activity_no_map.__contains__(activity_no):
            print("该活动不存在发放账户，activity_no=%s,ff_acc_no=%s" % (activity_no, ff_acc_no))
            continue

        # 排查名单发放
        if not ff_acc_list.__contains__(ff_acc_no):
            continue

        apply_amount = activity_no_map[activity_no][2] * 10
        # 金额
        if ff_acc_no_activity_sum.__contains__(ff_acc_no):
            ff_acc_no_activity_sum[ff_acc_no] = ff_acc_no_activity_sum[ff_acc_no] + apply_amount
        else:
            ff_acc_no_activity_sum[ff_acc_no] = apply_amount

        # 数量
        if ff_acc_no_activity_num.__contains__(ff_acc_no):
            ff_acc_no_activity_num[ff_acc_no] = ff_acc_no_activity_num[ff_acc_no] + 1
        else:
            ff_acc_no_activity_num[ff_acc_no] = 1

    # 查询所有的充值金额

    ff_acc_no_flag = dict()
    index_count = 0
    for ff_acc_no in ff_acc_no_activity_sum.keys():

        ff_acc_no_trans_sum = 0
        ff_acc_no_trans_num = 0

        # if ff_acc_no == "FF-210305-05605" or ff_acc_no == "FF-210910-27129":
        #     continue

        if is_check_out_ff_acc_no_list.__contains__(ff_acc_no):
            continue

        index_count += 1
        # if index_count >= 101:
        #     break

        print(ff_acc_no)

        #查询不同表
        cz_sql = grant_list_sql.account_ff_cz_sql.format("'" + ff_acc_no + "'")
        if ff_acc_no == "FF-210305-05605" or ff_acc_no == "FF-210910-27129":
            cz_sql = grant_list_sql.account_tmp_ff_cz_sql.format("'" + ff_acc_no + "'")

        col_list_m, row_list_m = dbutils.execute_sql(cz_sql, "查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            print("查询充值数据为空:%s" % str(ff_acc_no))
        else:
            for index, item in enumerate(row_list_m):
                ff_acc_no_trans_sum = ff_acc_no_trans_sum + item[1]*10
                ff_acc_no_trans_num = ff_acc_no_trans_num + 1
            activity_apply_sum = ff_acc_no_activity_sum[ff_acc_no]/10
            if activity_apply_sum == ff_acc_no_trans_sum/10:
                ff_acc_no_flag[ff_acc_no] = 1
            else:
                print("发放账户:%s，充值流水条数:%d,金额：%.1f,活动申请条数:%d，活动申请金额:%.1f" % (ff_acc_no, ff_acc_no_trans_num, ff_acc_no_trans_sum/10, ff_acc_no_activity_num[ff_acc_no],activity_apply_sum))
                ff_acc_no_flag[ff_acc_no] = 0
    #临时集合
    ff_out_trans_no_map = dict()

    #结果集合
    ff_acc_no_list = []
    activity_no_list = []
    sum_trans_amount_list = []
    sum_list_amount_list = []
    out_trans_no_list = []
    ff_acc_no_is_order = []
    grant_method_name_list = []
    for iCol in range(ncols):
        activity_no = excel.iloc[iCol, activity_no_col]
        ff_acc_no = excel.iloc[iCol, ff_acc_no_col]

        # 过滤特殊情况
        if not activity_no_map.__contains__(activity_no):
            print("该活动不存在发放账户，activity_no=%s,ff_acc_no=%s" % (activity_no, ff_acc_no))
            continue

        # 排出名单发放
        if not ff_acc_list.__contains__(ff_acc_no):
            continue

        if not ff_acc_no_flag.keys().__contains__(ff_acc_no):
            continue

        # 查询流水中活动的发放金额
        sum_trans_amount = 0
        extra = '{"activity_no":"%s","source":"platform_grant"}' % (activity_no)
        col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.account_ff_ff_sql.format("'" + ff_acc_no + "'","'" + extra + "'"), "查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            print("查询发放数据为空:ff_acc_no = %s,activity_no = %s" % (str(ff_acc_no),activity_no))
        else:
            if not row_list_m[0][1] is None:
                sum_trans_amount = row_list_m[0][1]

        # 查询订单模块中流水的发放金额
        sum_list_amount = 0
        col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.account_ff_order_sql.format("'" + activity_no + "'"), "查询流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            print("查询订单发放数据为空:ff_acc_no = %s,activity_no = %s" % (str(ff_acc_no), activity_no))
        else:
            if not row_list_m[0][1] is None:
                sum_list_amount = row_list_m[0][1]

        if sum_trans_amount != sum_list_amount:
            print("ff_acc_no:%s,activity_no:%s,ff_sum:%.1f,order_sum:%.1f" % (str(ff_acc_no),activity_no,sum_trans_amount,sum_list_amount))
            out_trans_nos = []
            if ff_out_trans_no_map.__contains__(ff_acc_no):
                out_trans_nos = ff_out_trans_no_map[ff_acc_no]
            else:
                # 查询该发放账户无extra的流水，最多10条
                col_list_m, row_list_m = dbutils.execute_sql(grant_list_sql.account_ff_out_trans_no_sql.format("'" + ff_acc_no + "'"), "查询流水", db_info[1], db_info[2])
                if row_list_m is None or len(row_list_m) == 0:
                    print("查询订单发放数据为空:ff_acc_no = %s,activity_no = %s" % (str(ff_acc_no), activity_no))
                else:
                    for index,item in enumerate(row_list_m):
                        out_trans_nos.append(item[0])
                    ff_out_trans_no_map[ff_acc_no] = out_trans_nos
            out_trans_no_list.append(",".join(out_trans_nos))
        else:
            out_trans_no_list.append("-")

        ff_acc_no_list.append(ff_acc_no)
        activity_no_list.append(activity_no)
        sum_trans_amount_list.append(sum_trans_amount)
        sum_list_amount_list.append(sum_list_amount)
        ff_acc_no_is_order.append(ff_acc_no_flag[ff_acc_no])
        if activity_no_map[activity_no][1] == 1:
            grant_method_name_list.append("接口")
        else:
            grant_method_name_list.append("名单")

    result_map = dict()
    result_map["发放账户"] = ff_acc_no_list
    result_map["活动编号"] = activity_no_list
    result_map["发放方式"] = grant_method_name_list
    result_map["流水发放金额"] = sum_trans_amount_list
    result_map["订单发放金额"] = sum_list_amount_list
    result_map["流水号"] = out_trans_no_list
    result_map["是否全部为活动发放"] = ff_acc_no_is_order

    writeUtil.writeToExcel(result_map, "FF-210305-05605-FF-210910-27129", "流水缺失发放编号-部分短缺")
