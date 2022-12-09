import datetime
import os

import dbutils_uat as dbutils_uat
import dbutils_prod as dbutils_prod
import strutils
import dbutils
import WashGrantOrderSql as order_sql
from ConstansList import activity_no_map
from ConstansList import ff_acc_no_list
from grant.order import CompanyTransactionDTO
from insert_grant_list import dealData
import json
import Sequence as sequence

# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/FF-210626-08786.json"
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


def grantListToCompanyTransaction(ff_acc_no,activity_no):

    out_trans_no_list = []

    #1、 查询差异数据
    col_list_m, row_list_g = dbutils.execute_sql(order_sql.t_company_transaction_extra_is_null_sql.format( "'" + ff_acc_no + "'"), "查询差异流水")
    if row_list_g is None or len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,无差别数据" % (ff_acc_no,activity_no))
    else:
        print("发放账户,ff_acc_no = %s,activity_no = %s,差别数据条数 = %s" % (ff_acc_no,activity_no, str(len(row_list_g))))

        if len(row_list_g) >= 1000:
            print("差别数据大于1000,具体数值:%d" % len(row_list_g))

        # amount = 1499900
        #2、 查询项目公司表id
        for index,item in enumerate(row_list_g):

            # amount -= item[8]
            # if amount < 0:
            #     break
            # print("本次金額:{1},剩餘金額:{0}".format(amount, item[8]))

            update_data = {
                "data": {
                    "id": item[0],
                    "extra": getExtra(activity_no)
                }
            }
            # 3、调用接口清洗数据
            dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)

            #清洗grant_list使用
            out_trans_no_list.append(item[4])

            print("清洗项目公司extra数据成功:{0}".format(update_data))

        return out_trans_no_list


def checkActivity(ff_acc_no, activity_no):
    col_list_m, row_list_g = dbutils.execute_sql(order_sql.check_activity_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'", "'" + getExtra(activity_no) + "'"), "确认是否合格")
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


def queryCompanyTransaction(wallet_trans_no):

    #1、 查询差异数据
    col_list_m, row_list_c = dbutils.execute_sql(order_sql.t_company_transaction_by_out_trans_no_sql.format("'" + wallet_trans_no + "'"), "查询项目公司流水",True)
    if row_list_c is None or len(row_list_c) != 1:
        print("项目公司数据,查询错误,out_trans_no = %s" % (wallet_trans_no))
    else:
        print("项目公司数据,t_company_transaction:{0} = %s".format(row_list_c))
        com_js = row_list_c[0]

        ct_js = json.loads(str(com_js).replace("\'","").replace("\\\\","\\\\\\"), object_hook=CompanyTransactionDTO.CompanyTransactionDTO)
        return ct_js

def query_user_info(target_acc_no):

    col_list_m, row_list_c = dbutils.execute_sql(order_sql.lf_account_sql.format("'" + target_acc_no + "'"), "查询用户账户")
    if row_list_c is None or len(row_list_c) != 1:
        print("查询用户账户,查询错误,out_trans_no = %s" % (wallet_trans_no))
        raise TypeError
    else:
        longminId = row_list_c[0][1]
        oa_account = row_list_c[0][2]
        personName = row_list_c[0][4]

    # 外部用户
    if str(target_acc_no).startswith("YH"):

        # 查询大会员手机号
        heard = {
            "Content-Type": "application/json",
            "X-GAIA-API-KEY": "dfd42c45-b7bb-4643-8673-7a44a900e873",
            "X-Client-IP": "127.0.0.1"
        }
        member_params = {
            "lmid_list": [
                longminId
            ],
            "desensitization": "false"
        }

        member_params = json.dumps(member_params)

        member_body = dbutils_prod.invoke_post("https://api.longhu.net/lmember-member-api-prod/internal/member/v1/phone-list", heard, member_params)
        try:
            print("查询大会员longminid查询手机号返回值:%s" % str(member_body))
            mem_js = json.loads(member_body)
        except:
            raise TimeoutError

        if "code" in mem_js and mem_js["code"] == "0000":
            data_ = mem_js["data"][0]
            phone = data_["phone"]

    elif str(target_acc_no).startswith("XF") or str(target_acc_no).startswith("GLZ"):
        phone = None

    return longminId, oa_account,personName, phone



def dealData(ctDTO):
    #发放账户
    col_list_m, row_list_c = dbutils.execute_sql(order_sql.lfm_account_info_sql.format("'" + ctDTO.getattribute("accNo") + "'"), "查询发放账户")
    if row_list_c is None or len(row_list_c) != 1:
        print("查询发放账户,查询错误,out_trans_no = %s" % (ctDTO.getattribute("outTransNo")))
        raise TypeError
    else:
        ctDTO.setattribute("activityType",row_list_c[0][0])
        ctDTO.setattribute("paymentUnitName",row_list_c[0][1])
        ctDTO.setattribute("ncCode",row_list_c[0][2])

    #查询用户账户
    longminId,oaAccount,personName,phone = query_user_info(ctDTO.getattribute("targetAccNo"))

    # 设置longminid，phone,personName
    ctDTO.setattribute("phone", phone)
    ctDTO.setattribute("longminId",longminId)
    ctDTO.setattribute("oaAccount",oaAccount)
    ctDTO.setattribute("personName",personName)


def insertGrantList(wallet_trans_no):

    print("流水号,out_trans_no = %s,清洗数据开始" % (wallet_trans_no))

    col_list_m, row_list_b = dbutils.execute_sql(order_sql.t_platform_grant_list_is_null_sql.format("'" + wallet_trans_no + "'"),"查询订单模块")
    if row_list_b != None and len(row_list_b) > 0:
        print("插入订单模块流水号:%s,已存在" % wallet_trans_no)
        return

    # 1、查询项目公司流水
    ctDTO = queryCompanyTransaction(wallet_trans_no)

    if ctDTO.getattribute("extra") is None or ctDTO.getattribute("extra") == "":
        raise AttributeError
        # #TODO
        # activity_no = "YH2112171417CJ68001"
    else:
        activity_no = json.loads(str(ctDTO.getattribute("extra")).replace("\\", ""))["activity_no"]

    # 2、查询账户信息
    dealData(ctDTO)

    # 3、组装请求参数
    params = ctDTO.buildGrantList(activity_no, sequence.createTroNo())

    # 3、请求insert接口
    dbutils_prod.execute("/api/wash/order/grant/list", params)

    print("清洗订单模块frant_list数据结束,流水号,out_trans_no = %s" % (wallet_trans_no))

if __name__ == "__main__":

    # activity_no = "YH2112301156CJ08701"
    # ff_acc_no = "FF-211226-40684"
    #
    # col_list_m, row_list_b = dbutils.execute_sql(order_sql.t_platform_grant_list_right_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'","'" + getExtra(activity_no) + "'"), "查询订单模块")
    # if row_list_b == None or len(row_list_b) < 1:
    #     print("插入订单模块流水号:%s,已存在" % activity_no)
    # else:
    #     wallet_trans_no_list = []
    #     for index, trans_no in enumerate(row_list_b):
    #         print("处理个数:%d，时间:%s" % (index,str(datetime.datetime.now())))
    #         insertGrantList(trans_no[0])
    #     # 3、确认数据
    #     checkActivity(ff_acc_no,activity_no)


    #洗入数据
    # activity_no = "YH2112171417CJ68001"

    # 循环处理数据
    for ff_acc_no, activity_no in ff_acc_no_list.items():

        print("发放账户,ff_acc_no = %s,清洗数据开始" % (ff_acc_no))

        #1、清洗项目公司数据
        wallet_trans_no_list = grantListToCompanyTransaction(ff_acc_no, activity_no)

        # #2、清洗grant_list
        # if wallet_trans_no_list == None or len(wallet_trans_no_list) < 1:
        #     raise AttributeError
        # for wallet_trans_no in wallet_trans_no_list:
        #     insertGrantList(wallet_trans_no)

        # #3、确认数据
        # checkActivity(ff_acc_no,activity_no)

        print("发放账户,ff_acc_no = %s,清洗数据结束\n" % (ff_acc_no))

