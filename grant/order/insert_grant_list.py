import json
import threading

import CompanyTransactionDTO as com
import os

import dbutils_uat as dbutils_uat
import dbutils_prod as dbutils_prod
import strutils
import dbutils
import WashGrantOrderSql as order_sql
from ConstansList import wallet_trans_no_list
from ConstansList import grant_list_id_list
import Sequence as sequence
import time
import threading as Thread
from concurrent.futures import ThreadPoolExecutor


# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/FF-210626-08786_grant_list_2.json"
    file = None
    try:
        file = open(path, mode="a", encoding="utf-8")
        file.write(msg + "\n")
    except Exception as e:
        print(e)
    finally:
        if file is not None:
            file.close()


def queryCompanyTransaction(out_trans_no):
    # 1、 查询差异数据
    col_list_m, row_list_c = dbutils.execute_sql(
        order_sql.t_company_transaction_by_out_trans_no_sql.format("'" + out_trans_no + "'"), "查询项目公司流水", True)
    if row_list_c is None or len(row_list_c) != 1:
        print("项目公司数据,查询错误,out_trans_no = %s" % (out_trans_no))
    else:
        print("项目公司数据,t_company_transaction:{0} = %s".format(row_list_c))
        com_js = row_list_c[0]

        ct_js = json.loads(str(com_js).replace("\'", "").replace("\\\\", "\\\\\\"),
                           object_hook=com.CompanyTransactionDTO)
        return ct_js


def query_user_info(target_acc_no):
    col_list_m, row_list_c = dbutils.execute_sql(order_sql.lf_account_sql.format("'" + target_acc_no + "'"), "查询用户账户")
    if row_list_c is None or len(row_list_c) != 1:
        print("查询用户账户,查询错误,out_trans_no = %s" % (out_trans_no))
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

        member_body = dbutils_prod.invoke_post(
            "https://api.longhu.net/lmember-member-api-prod/internal/member/v1/phone-list", heard, member_params)
        try:
            print("查询大会员longminid查询手机号返回值:%s" % str(member_body))
            mem_js = json.loads(member_body)
        except:
            raise TimeoutError

        if "code" in mem_js and mem_js["code"] == "0000":
            if len(mem_js["data"]) == 0:
                phone = None
            else:
                data_ = mem_js["data"][0]
                phone = data_["phone"]

    elif str(target_acc_no).startswith("XF") or str(target_acc_no).startswith("GLZ"):
        phone = None

    return longminId, oa_account, personName, phone


def dealData(ctDTO):
    # 发放账户
    col_list_m, row_list_c = dbutils.execute_sql(
        order_sql.lfm_account_info_sql.format("'" + ctDTO.getattribute("accNo") + "'"), "查询发放账户")
    if row_list_c is None or len(row_list_c) != 1:
        print("查询发放账户,查询错误,out_trans_no = %s" % (out_trans_no))
        raise TypeError
    else:
        ctDTO.setattribute("activityType", row_list_c[0][0])
        ctDTO.setattribute("paymentUnitName", row_list_c[0][1])
        ctDTO.setattribute("ncCode", row_list_c[0][2])

    # 查询用户账户
    longminId, oaAccount, personName, phone = query_user_info(ctDTO.getattribute("targetAccNo"))

    # 设置longminid，phone,personName
    ctDTO.setattribute("phone", phone)
    ctDTO.setattribute("longminId", longminId)
    ctDTO.setattribute("oaAccount", oaAccount)
    if personName is not None:
        ctDTO.setattribute("personName", personName)


"""
获取扩展字段
"""


def getExtra(activity_no):
    return '{"activity_no":"%s","source":"platform_grant"}' % activity_no


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


# if __name__ == "__main__":
def insertGrantList(minId = 0, maxId = 0):
    id_list = [
        59443245,
        59443248,
        59443249,
        59443250,
        59443251,
        59443240,
        59443243,
        59443244,
        59427591,
        59427598,
        59427602,
        59443246,
        59443241,
        59443247
    ]
    for id in id_list:
        params = {
            "id": id,
            "grantStatus": 1
        }
        # 3、请求insert接口
        dbutils_prod.execute("/api/wash/order/grant/list", params)
    # 1、 查询差异数据
    activity_no = 'YH2112300936CJ72001'
    ff_acc_no = 'FF-210626-08786'

    col_list_m, row_list_g = dbutils.execute_sql(
        order_sql.t_platform_grant_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'",
                                                         "'" + getExtra(activity_no) + "'"), "查询差异流水")
    if row_list_g is None:
        print("当前线程:%s,minId:%d,maxId:%d,待清洗条目:%d" % (Thread.current_thread().getName(), minId, maxId, "None"))
    else:
        print("当前线程:%s,minId:%d,maxId:%d,待清洗条目:%d" % (Thread.current_thread().getName(), minId, maxId, len(row_list_g)))
    if row_list_g is None or len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,无差别数据" % (ff_acc_no, activity_no))
    else:
        # 循环处理数据
        for idx, item in enumerate(row_list_g):
            out_trans_no = item[0]
            print("流水号,out_trans_no = %s,清洗数据开始" % (out_trans_no))

            # 1、查询项目公司流水
            ctDTO = queryCompanyTransaction(out_trans_no)

            if ctDTO.getattribute("extra") is None:
                # activity_no = "YG2011200932CJ67301"
                raise AttributeError
            else:
                activity_no = json.loads(str(ctDTO.getattribute("extra")).replace("\\", ""))["activity_no"]

            # 2、查询账户信息
            dealData(ctDTO)

            # 3、组装请求参数
            params = ctDTO.buildGrantList(activity_no, sequence.createTroNo())

            # 3、请求insert接口
            dbutils_prod.execute("/api/wash/order/grant/list", params)

            print("流水号,out_trans_no = %s,清洗数据结束" % (out_trans_no))
        # 3、确认数据
        checkActivity(ff_acc_no, activity_no)


def queryIdMap(maxId=0):
    activity_no = 'YH2112300936CJ72001'
    ff_acc_no = 'FF-210626-08786'
    col_list_m, row_list_g = dbutils.execute_sql(
        order_sql.t_platform_grant_list_right_id_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'",
                                                            "'" + getExtra(activity_no) + "'", maxId), "查询差异流水")
    if row_list_g is None or len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,无差别数据" % (ff_acc_no, activity_no))
        return
    else:
        minId = row_list_g[0][0]
        maxId = row_list_g[len(row_list_g) - 1][1]
        print("minId:%d,maxId:%d" % (minId, maxId))
        # 递归
        queryIdMap(maxId)


def main():
    # queryIdMap()

    threads = []
    id_map = {
        # 103960771:205266991,
        # 205267923:206734709,
        # 206735301:208442000,
        # 208442069:209039379,
        # 209040067:210329614
        # 210329746:212354874,
        # 212356225:213317414,
        # 213317844:215859934,
        # 215861670:218283238,
        # 218287968:222192132,
        # 222198596:224609511
        # 224609826:225967456,
        # 225967945:227236526,
        # 227237345:228657871,
        # 228658399:230061527,
        # 230062355:231553953,
        # 231554272:232390831,
        # 232391611:233207356,
        # 233208588:234351693,
        # 234351968:235945216
        # 235948798:237543115
        # 237543796:238591745,
        # 238592568:239497302,
        # 239497485:240708944,
        # 240709772:241892866,
        # 241892969:242931971,
        # 242932359:243865564,
        # 243865684:244948267,
        # 244949222:246049203,
        # 246049814:247068110,
        # 247068343:247932765
        # 247932793:248597691,
        # 248597697:249433344,
        # 249433593:250862002,
        # 250862323:252035022,
        # 252035448:252784565,
        # 252785526:253621411,
        # 253621877:254369941,
        # 254370605:255055822,
        # 255056722:256134507
        # 256136093:257270545,
        # 257270874:258101012,
        # 258101142:259024707,
        # 259025598:260018959,
        # 260019391:261842246,
        # 261843756:263416836,
        # 263417228:264289835,
        # 264290064:265277857,
        # 265280046:266564867,
        # 266565169:267981160,
        # 267981356:268952269,
        # 268952402:269780405,
        # 269781314:270818095,
        # 270818140:271993621,
        # 271994496:273459935,
        # 273462269:274366817,
        # 274369520:275203229,
        # 275203352:275993929,
        # 275994848:276788311,
        # 276788511:277933078,
        # 277934705:279704254,
        # 279704816:281345235,
        # 281349038:282976928,
        # 282979326:284380200,
        # 284380627:285566749,
        # 285568059:286743040,
        # 286743798:287723439,
        # 287723495:288773458,
        # 288774071:290055400,
        # 290057041:290942776,
        # 290944061:292074841,
        # 292074917:292887586,
        # 292888038:294172917,
        # 294174542:295175702,
        # 295175714:295876979,
        # 295877004:296647810,
        # 296647856:297932723,
        # 297932780:299x049324,
        # 299051409:299949233,
        # 299950796:301117988,
        # 301118835:302066450,
        # 302066565:303336497,
        # 303337519:304836365
        # 297164384:300357081,
        # 300357543:302826662,
        # 302826764:304832323,
        304832839:305489861,
        # 305490434:306182574,
        # 306184836:307107799,
        307109544:307953019
        # 307953412:308894099,
        # 308894246:309800477,
        # 309800653:310533558,
        # 310533888:311139348,
        # 311139509:311795019,
        # 311795886:312502704,
        # 312503132:313418997,
        # 313419109:314331433,
        # 314332124:315042374,
        # 315043082:315684644,
        # 315685679:316241945,
        # 316242549:316749367,
        # 316749571:324069314
    }

    # with ThreadPoolExecutor(max_workers=6) as pool:
    #     for k, v in id_map.items():
    #         start = time.time()
    #         pool.submit(insertGrantList, [k,v])
    #         end = time.time()
    #         print(f'总耗时: {end - start:.3f}秒.')

    for k, v in id_map.items():
        thread1 = Thread.Thread(target=insertGrantList, args=[k, v, ])
        threads.append(thread1)

    print("数据清洗开始")
    start = time.time()
    # 启动三个线程
    for thread in threads:
        thread.start()
    # 等待线程结束
    for thread in threads:
        thread.join()
    end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')


if __name__ == "__main__":
    main()
