import json

import dbutils
import WashGrantOrderSql as order_sql
import strutils
import dbutils_uat as dbutils_uat
import dbutils_prod as dbutils_prod


# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/company_and_grant_2.json"
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


"""
获取扩展字段
"""


def getExtra(activity_no):
    return '{"activity_no":"%s","source":"platform_grant"}' % activity_no


def checkGrantOrder(ff_acc_no, activity_no):
    # 1、 查询差异数据
    col_list_m, row_list_g = dbutils.execute_sql(
        order_sql.t_platform_grant_list_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'",
                                                   "'" + getExtra(activity_no) + "'"), "查询差异流水")
    if row_list_g is None or len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,无差别数据" % (ff_acc_no, activity_no))
    else:
        print("发放账户,ff_acc_no = %s,activity_no = %s,差别数据条数 = %s" % (ff_acc_no, activity_no, str(len(row_list_g))))

        if len(row_list_g) >= 1000:
            print("差别数据大于1000,具体数值:%d" % len(row_list_g))

        # 2、 查询项目公司表id
        col_list_m, row_list_c = dbutils.execute_sql(
            order_sql.t_company_transaction_new_sql.format(strutils.remove_bracket(row_list_g)), "查询项目公司流水id")
        if row_list_c is None or len(row_list_c) <= 0:
            print("发放账户,ff_acc_no = %s,activity_no = %s,无项目公司流水" % (ff_acc_no, activity_no))
            raise RuntimeError
        else:
            if len(row_list_g) != len(row_list_c):
                raise TypeError
                # pass
            for index, item in enumerate(row_list_c):
                print("id:%d,应该发放账户:%s,实际发放账户:%s" % (item[0], ff_acc_no, item[2]))
                update_data = {
                    "data": {
                        "id": item[0],
                        "extra": getExtra(activity_no)
                    }
                }

                # 3、调用接口清洗项目公司数据
                dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)
                print("设置t_company_transation,extra = null,成功:{0}".format(update_data))


def checkActivity(ff_acc_no, activity_no):
    col_list_m, row_list_g = dbutils.execute_sql(
        order_sql.check_activity_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'",
                                            "'" + getExtra(activity_no) + "'"), "确认是否合格")
    if row_list_g is not None and len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,查询确认结果为空" % (ff_acc_no, activity_no))
        raise TypeError
    else:
        check_flag = False
        if row_list_g[0] is not None and row_list_g[0][0] is not None and row_list_g[0][1] is not None:
            if row_list_g[0][0] == row_list_g[0][1]:
                check_flag = True
        if check_flag:
            print("发放账户,ff_acc_no = %s,activity_no = %s,订单模块净发放:%s,项目公司流水净发放:%s,已确认,符合" % (
                ff_acc_no, activity_no, str(row_list_g[0][0]), str(row_list_g[0][1])))
        else:
            print("发放账户,ff_acc_no = %s,activity_no = %s,订单模块净发放:%s,项目公司流水净发放:%s,已确认,不符合" % (
                ff_acc_no, activity_no, str(row_list_g[0][0]), str(row_list_g[0][1])))


activity_no_list = [
    # "YH2204011638CJ79501",
    # "YH2204081459CJ96301",
    # "YH2204081403CJ72201",
    # "YH2204120950CJ17801",
    # "YH2204131828CJ35001",
    # "YH2204191417CJ23201",
    # "YH2204211439CJ57901",
    # "YH2204220944CJ05701",
    # "YH2205121051CJ22602",
    # "YH2205181031CJ28001", 活动编号实际发放账户05605
    "YH2205231358CJ25501",
    "YH2205261913CJ40001",
    "YH2205271929CJ56601",
    "YH2206020911CJ07901",
    "YH2206031452CJ19302",
    "YH2206061815CJ23101",
    "YH2206131457CJ23001",
    "YH2206161204CJ54301",
    "YH2206162106CJ57601",
    "YH2206160951CJ43801",
    "YH2206171532CJ44701",
    "YH2206161728CJ73601",
    "YH2206171157CJ66101",
    "YH2206201635CJ73601",
    "YH2206210945CJ00901",
    "YH2206281054CJ36401",
    "YH2206291333CJ64401",
    "YH2206301124CJ71501",
    "YH2206301146CJ16301",
    "YH2207011336CJ03301",
    "YH2207011348CJ17601",
    "YH2207011449CJ36901",
    "YH2207011129CJ84602",
    "YH2207051007CJ89301",
    "YH2207041100CJ16801",
    "YH2207041158CJ55001",
    "YH2207041104CJ68401",
    "YH2207061309CJ01001",
    "YH2207080916CJ04201",
    "YH2207111803CJ22401",
    "YH2207151400CJ16502",
    "YH2207211459CJ30301",
    "YH2207201455CJ28001",
    "YH2207211557CJ71901",
    "YH2207181824CJ84901",
    "YH2207192103CJ84601",
    "YH2207271158CJ21901",
    "YH2207291353CJ03601",
    "YH2208020941CJ37501",
    "YH2208020943CJ92901",
    "YH2208020927CJ73301",
    "YH2208011129CJ66001",
    "YH2208031244CJ71301",
    "YH2208031614CJ73501",
    "YH2208041927CJ76801",
    "YH2208090935CJ26201",
    "YH2208081026CJ41701",
    "YH2208081803CJ53501",
    "YH2208091745CJ36001",
    "YH2208121054CJ47301",
    "YH2208141706CJ63701",
    "YH2208171505CJ26801",
    "YH2208260916CJ05901",
    "YH2208251348CJ41801",
    "YG2208301029CJ84501",
    "YG2109091937CJ13301",
    "YG2110031853CJ64701",
    "YG2205161803CJ92801",
    "YG2205251748CJ01701",
    "YG2207121723CJ66201"
]

if __name__ == "__main__":

    ff_acc_no = "FF-210910-27129"
    for activity_no in activity_no_list:
        print("发放账户:%s,开始" % activity_no)
        checkGrantOrder(ff_acc_no, activity_no)

        # 2、确认数据
        checkActivity(ff_acc_no, activity_no)
        print("发放账户:%s,结束" % activity_no)
