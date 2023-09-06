import json
import os

import pandas
import pandas as pd
from test.longfor import dbutils
import test.GrantListSql as grant_list_sql
from test.longfor.DBConfig import db_list_info as  db_info_list
import WashGrantOrderSql as sql

print_rersult_list = []

# 打印到文件
def writeToExcel(result,sheet_name):
    file_name = "/Users/admin/Desktop/订单模块排查/活动维度排查结果_2023_08_16.xlsx"

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
# def print1(msg):
#     path = "/Users/admin/Desktop/订单模块排查/msg_result_01_04_1.json"
#     file = None
#     try:
#         # if not os.path.exists(path):
#         file = open(path, mode="a", encoding="utf-8")
#         file.write(msg + "\n")
#     except Exception as e:
#         print(e)
#     finally:
#         if file is not None:
#             file.close()

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
        grant_method_name_list.append(grant_method_name_map[activity_no])
        grant_status_list.append(grant_status_map[activity_no])
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
    grant_status_list.append("-")
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

if __name__ == "__main__":

    db_info = db_info_list[0]

    ff_acc_no_List_map = {
        "YH2009241135CJ65201",
        "YH2009241621CJ41701",
        "YH2011091553CJ40601",
        "YH2012211313CJ73101",
        "YH2106232113CJ85202",
        "YH2106241316CJ43301",
        "YH2106261356CJ47501",
        "YH2105241445CJ06201",
        "YH2106080912CJ91202",
        "YH2109131426CJ95602",
        "YH2105241533CJ21201",
        "YH2105091145CJ55702",
        "YH2109091530CJ92001",
        "YH2109162003CJ41301",
        "YH2105261129CJ55301",
        "YH2106081405CJ37801",
        "YH2108091709CJ67601",
        "YH2108161216CJ07701",
        "YH2105261054CJ73501",
        "YH2112151521CJ09501",
        "YH2105112042CJ36501",
        "YH2106202312CJ67901",
        "YH2107221018CJ00501",
        "YH2108120955CJ89302",
        "YH2105131000CJ51101",
        "YH2111171134CJ30002",
        "YH2109141733CJ60301",
        "YH2109291449CJ45901",
        "YH2110141610CJ73501",
        "YH2112191258CJ92601",
        "YH2202131123CJ87801",
        "YH2112141703CJ77401",
        "YH2112231334CJ27701",
        "YH2112231340CJ83701",
        "YH2111120954CJ08801",
        "YH2108271933CJ21201",
        "YH2109091719CJ20601",
        "YH2112161124CJ59501",
        "YH2112222357CJ15401",
        "YH2112231537CJ55801",
        "YH2112241002CJ23701",
        "YH2204061033CJ57001",
        "YH2105141548CJ39802",
        "YH2201251744CJ49301",
        "YH2106021111CJ16601",
        "YH2111160054CJ71101",
        "YH2112091754CJ37301",
        "YH2106041100CJ66401",
        "YH2106171934CJ90401",
        "YH2106211056CJ13301",
        "YH2105211048CJ21901",
        "YH2112241046CJ08202",
        "YH2111221140CJ95801",
        "YH2109172024CJ71701",
        "YH2110131433CJ04801",
        "YH2203110941CJ41902",
        "YH2203291139CJ08401",
        "YH2106060749CJ55401",
        "YH2104191455CJ25301",
        "YH2104221613CJ86501",
        "YH2106071429CJ63903",
        "YH2105060932CJ16401",
        "YH2110221110CJ38101",
        "YH2108271448CJ72001",
        "YH2110111625CJ95701",
        "YH2106081812CJ85501",
        "YH2107231255CJ96401",
        "YH2108231859CJ81601",
        "YH2112141107CJ53801",
        "YH2112161420CJ36002",
        "YH2112171941CJ23601",
        "YH2112201228CJ58002",
        "YH2112201233CJ99501",
        "YH2112251327CJ69501",
        "YH2112271641CJ59901",
        "YH2203291525CJ14801",
        "YH2106090918CJ38901",
        "YH2106102335CJ13801",
        "YH2106160917CJ22301",
        "YH2106091411CJ43601",
        "YH2111021717CJ32101",
        "YH2204011550CJ93901",
        "YH2106091548CJ58901",
        "YH2104191705CJ18901",
        "YH2104191735CJ87801",
        "YH2106091553CJ96701",
        "YH2112091437CJ17305",
        "YH2112311028CJ69801",
        "YH2106091558CJ40001",
        "YH2106091604CJ75201",
        "YH2111251740CJ66401",
        "YH2112150938CJ71801",
        "YH2106101420CJ44301",
        "YH2106201550CJ55301",
        "YH2105192057CJ89701",
        "YH2202242011CJ85901",
        "YH2106150953CJ49001",
        "YH2105111636CJ67402",
        "YH2106171352CJ45001",
        "YH2106171454CJ13501",
        "YH2112211713CJ11901",
        "YH2112211719CJ82301",
        "YH2112211729CJ97902",
        "YH2108270910CJ23001",
        "YH2105170957CJ57001",
        "YH2106181440CJ76801",
        "YH2105060935CJ08701",
        "YH2106221921CJ38701",
        "YH2111101006CJ76101",
        "YH2112221041CJ94201",
        "YH2112300936CJ72001",
        "YH2106231110CJ00001",
        "YH2112060929CJ91601",
        "YH2112161613CJ95303",
        "YH2106251903CJ38101",
        "YH2106261132CJ83801",
        "YH2112221149CJ02402",
        "YH2106292101CJ05001",
        "YH2109071726CJ11301",
        "YH2110231602CJ87401",
        "YH2111261424CJ73001",
        "YH2112161633CJ23501",
        "YH2112171536CJ75501",
        "YH2112171547CJ80501",
        "YH2112171555CJ83302",
        "YH2112171600CJ77802",
        "YH2109241542CJ04402",
        "YH2111241038CJ89801",
        "YH2112061840CJ47901",
        "YH2112291042CJ04001",
        "YH2203110930CJ12901",
        "YH2109241547CJ61201",
        "YH2110201654CJ08101",
        "YH2110201717CJ19701",
        "YH2112151902CJ95801",
        "YH2112282231CJ07001",
        "YH2112282242CJ72401",
        "YH2203061111CJ44401",
        "YH2203111104CJ28801",
        "YH2107091135CJ73301",
        "YH2112061720CJ63601",
        "YH2107061036CJ83102",
        "YH2103110941CJ77101",
        "YH2109151230CJ34801",
        "YH2110250933CJ37101",
        "YH2201240943CJ74101",
        "YH2201081153CJ68001",
        "YH2107091740CJ18101",
        "YH2105141624CJ75001",
        "YH2107161409CJ09602",
        "YH2107211717CJ25901",
        "YH2109131335CJ38501",
        "YH2111031824CJ18601",
        "YH2111151434CJ86601",
        "YH2112181722CJ55801",
        "YH2202151616CJ09201",
        "YH2107271823CJ28301",
        "YH2102201513CJ38001",
        "YH2112171417CJ68001",
        "YH2107281444CJ97401",
        "YH2108071023CJ51101",
        "YH2107301153CJ03901",
        "YH2108130910CJ81201",
        "YH2110250824CJ03601",
        "YH2111250946CJ30201",
        "YH2111081011CJ11601",
        "YH2111101111CJ45001",
        "YH2111172235CJ86201",
        "YH2112271717CJ56501",
        "YH2112171541CJ42101",
        "YH2110271012CJ72401",
        "YH2110201116CJ52501",
        "YH2109131419CJ37201",
        "YH2109151454CJ77103",
        "YH2111151609CJ91501",
        "YH2112161604CJ94404",
        "YH2203241157CJ17901",
        "YH2108311709CJ21602",
        "YH2111031925CJ32802",
        "YH2109091712CJ34601",
        "YH2203042057CJ93201",
        "YH2112261425CJ44201",
        "YH2105141427CJ07701",
        "YH2109152349CJ27501",
        "YH2112141729CJ26501",
        "YH2112231321CJ16601",
        "YH2112271451CJ40101",
        "YH2203041114CJ31101",
        "YH2203301419CJ96401",
        "YH2109161032CJ05801",
        "YH2201072004CJ33001",
        "YH2203151419CJ70501",
        "YH2109161134CJ02602",
        "YH2109281939CJ42601",
        "YH2204011601CJ26101",
        "YH2110181352CJ46101",
        "YH2112241634CJ08601",
        "YH2109231727CJ51402",
        "YH2109251649CJ63101",
        "YH2109291046CJ46301",
        "YH2112061830CJ01401",
        "YH2112171554CJ95801",
        "YH2109291044CJ49301",
        "YH2112171602CJ56001",
        "YH2201260938CJ48902",
        "YH2109291036CJ93901",
        "YH2112070921CJ03101",
        "YH2112171600CJ69101",
        "YH2201260927CJ67801",
        "YH2103181226CJ80701",
        "YH2204111025CJ40601",
        "YH2103231619CJ12001",
        "YH2104090944CJ09901",
        "YH2110221718CJ65201",
        "YH2110251646CJ27001",
        "YH2203091014CJ12701",
        "YH2201191624CJ68101",
        "YH2111101611CJ34401",
        "YH2111121138CJ37401",
        "YH2111171446CJ83801",
        "YH2111202213CJ26501",
        "YH2111232113CJ30201",
        "YH2111241102CJ26501",
        "YH2112071011CJ35401",
        "YH2112161139CJ37501",
        "YH2112291753CJ61001",
        "YH2203021558CJ05402",
        "YH2111251025CJ65201",
        "YH2202111726CJ89001",
        "YH2202111743CJ91901",
        "YH2202111748CJ15601",
        "YH2202111752CJ14501",
        "YH2111251026CJ80201",
        "YH2111291050CJ19101",
        "YH2112011208CJ11001",
        "YH2112011211CJ19501",
        "YH2112101030CJ02102",
        "YH2112211123CJ05001",
        "YH2112061642CJ53301",
        "YH2112071112CJ35701",
        "YH2112281303CJ42801",
        "YH2112301148CJ75601",
        "YH2112141723CJ11201",
        "YH2203301416CJ39801",
        "YH2112301909CJ04201",
        "YH2112191309CJ03701",
        "YH2112201754CJ18301",
        "YH2112201820CJ10601",
        "YH2112221155CJ88601",
        "YH2112241217CJ59401",
        "YH2112301156CJ08701",
        "YH2112281423CJ24701",
        "YH2201050926CJ90601",
        "YH2202171655CJ77601",
        "YH2201141059CJ65201",
        "YH2104221334CJ99701",
        "YH2202161141CJ71701",
        "YH2201141051CJ32202",
        "YH2202111544CJ91201",
        "YH2202151618CJ46301",
        "YH2203171502CJ48901",
        "YH2212221350CJ95701"
    }

    ff_acc_no_map = dict()
    grant_method_name_map = dict()
    grant_status_map = dict()
    col_list_m, row_list_g = dbutils.execute_sql(sql.select_budget_appply_ff_acc_sql, "查询活动")

    if row_list_g is  None or len(row_list_g) <= 0:
        raise TypeError
    else:
        for item in row_list_g:

            activity_no = item[0]
            ff_acc_no = item[1]

            if not ff_acc_no_List_map.__contains__(activity_no):
                continue

            if ff_acc_no_map.__contains__(ff_acc_no):
                ff_acc_no_map[ff_acc_no].append(activity_no)
            else:
                ff_acc_no_map[ff_acc_no] = [activity_no]

            # if grant_method_name_map.__contains__(activity_no):
            #     print("grant_method:" + activity_no)
            # if grant_status_map.__contains__(activity_no):
            #     print("grant_status:" + activity_no)
            grant_method_name_map[activity_no] = item[2]
            grant_status_map[activity_no] = item[3]

    # 待发放金额 = 申请金额 - 已发金额 - 未注册待发放 - 已回冲金额 - 回冲中 - 销账金额
    result_map = dict()
    ff_acc_no_list = []
    activity_nos = []
    is_grant_flag_list = []
    grant_method_name_list = []
    grant_status_list = []
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

    index_flag = 0
    for ff_acc_no,activity_no_list in ff_acc_no_map.items():
        index_flag+=1
        # if index_flag > 300:
        #     break
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
    result_map["发放状态"] = grant_status_list
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
    writeToExcel(result_map,"sheet1")

