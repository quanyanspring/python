import json
import CompanyTransactionDTO as com
import os

import dbutils_uat as dbutils_uat
import dbutils_prod as dbutils_prod
import strutils
import dbutils
import WashGrantOrderSql as order_sql
from ConstansList import wallet_trans_no_list
from  ConstansList import  grant_list_id_list

# 写入文件
# def print(msg):
#     path = "/Users/admin/Desktop/订单模块排查/msg_result.json"
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

def queryCompanyTransaction(trans_no):

    #1、 查询差异数据
    col_list_m, row_list_c = dbutils.execute_sql(order_sql.t_company_transaction_by_out_trans_no_sql.format("'" + trans_no + "'"), "查询项目公司流水",True)
    if row_list_c is None or len(row_list_c) != 1:
        print("项目公司数据,查询错误,out_trans_no = %s" % (trans_no))
    else:
        print("项目公司数据,t_company_transaction:{0} = %s".format(row_list_c))
        com_js = row_list_c[0]

        ct_js = json.loads(str(com_js).replace("\'","").replace("\\\\","\\\\\\"), object_hook=com.CompanyTransactionDTO)
        return ct_js

def query_user_info(target_acc_no):

    col_list_m, row_list_c = dbutils.execute_sql(order_sql.lf_account_sql.format("'" + target_acc_no + "'"), "查询用户账户")
    if row_list_c is None or len(row_list_c) != 1:
        print("查询用户账户,查询错误,out_trans_no = %s" % (trans_no))
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
            print("查询大会员longminid查询手机号返回值：%s" % str(member_body))
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
        print("查询发放账户,查询错误,out_trans_no = %s" % (trans_no))
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


if __name__ == "__main__":

    params = {
        "id": 54571215,
        "isDeleted": 1
    }
    # 3、请求insert接口
    dbutils_prod.execute("/api/wash/order/grant/list", params)

    # 循环处理数据
    for trans_no in wallet_trans_no_list:

        print("流水号,out_trans_no = %s,清洗数据开始" % (trans_no))

        #1、查询项目公司流水
        ctDTO = queryCompanyTransaction(trans_no)

        if ctDTO.getattribute("extra") is None:
            activity_no = "YG2011200932CJ67301"
        else:
            activity_no = json.loads(str(ctDTO.getattribute("extra")).replace("\\",""))["activity_no"]


        #2、查询账户信息
        dealData(ctDTO)

        #3、组装请求参数
        params = ctDTO.buildGrantList(activity_no, "YG2011200932CJ67301-000002")

        #3、请求insert接口
        dbutils_prod.execute("/api/wash/order/grant/list", params)

        print("流水号,out_trans_no = %s,清洗数据结束" % (trans_no))

