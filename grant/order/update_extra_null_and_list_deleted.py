import dbutils_prod as dbutils_prod
from test.longfor import strutils, dbutils
import WashGrantOrderSql as order_sql
from ConstansList import company_grant_list_map

# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/msg_result.json"
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


def grantListToCompanyTransaction(ff_acc_no, activity_no):

    #1、 查询差异数据
    col_list_m, row_list_g = dbutils.execute_sql(order_sql.t_platform_grant_list_sql.format("'" + activity_no + "'", "'" + ff_acc_no + "'", "'" + getExtra(activity_no) + "'"), "查询差异流水")
    if row_list_g is None or len(row_list_g) <= 0:
        print("发放账户,ff_acc_no = %s,activity_no = %s,无差别数据" % (ff_acc_no, activity_no))
    else:
        print("发放账户,ff_acc_no = %s,activity_no = %s,差别数据条数 = %s" % (ff_acc_no, activity_no, str(len(row_list_g))))

        if len(row_list_g) >= 1000:
            print("差别数据大于1000,具体数值:%d" % len(row_list_g))

        #2、 查询项目公司表id
        col_list_m, row_list_c = dbutils.execute_sql(order_sql.t_company_transaction_new_sql.format(
            strutils.remove_bracket(row_list_g)), "查询项目公司流水id")
        if row_list_c is None or len(row_list_c) <= 0:
            print("发放账户,ff_acc_no = %s,activity_no = %s,无项目公司流水" % (ff_acc_no, activity_no))
            raise RuntimeError
        else:
            if len(row_list_g) != len(row_list_c):
                raise TypeError
            for index, item in enumerate(row_list_c):
                print("id:%d,应该发放账户:%s,实际发放账户:%s" % (item[0], ff_acc_no, item[2]))
                update_data = {
                    "data": {
                        "id": item[0],
                        "extra": " "
                    }
                }

                #3、调用接口清洗项目公司数据
                dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)
                print("设置t_company_transation,extra = null,成功:{0}".format(update_data))

                #4、调用接口设置订单模块数据
                col_list_m, row_list_l = dbutils.execute_sql(order_sql.t_platform_grant_list_all_sql.format("'" + item[1] + "'"), "查询订单模块数据")
                if row_list_l is None or len(row_list_l) != 1:
                    print("发放账户,ff_acc_no = %s,activity_no = %s,无订单模块数据" % (ff_acc_no, activity_no))
                    raise RuntimeError
                else:
                    grant_list_id = row_list_l[0][0]
                    grant_list_params = {
                        "id": grant_list_id,
                        "isDeleted": 1,
                        "remark": "接口发放错误使用发放账户,活动对应发放账户:{0},实际使用发放账户:{1}".format(ff_acc_no, item[2])
                    }
                    dbutils_prod.execute("/api/wash/order/grant/list", grant_list_params)
                    print("设置t_grang_list,isdeleted = 1,成功:{}".format(grant_list_params))




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




if __name__ == "__main__":

    # 循环处理数据
    for activity_no,ff_acc_no in company_grant_list_map.items():

        print("发放账户,ff_acc_no = %s,activity_no = %s,清洗数据开始" % (ff_acc_no,activity_no))

        #1、清洗数据
        grantListToCompanyTransaction(ff_acc_no,activity_no)
        #2、确认数据
        checkActivity(ff_acc_no,activity_no)

        print("发放账户,ff_acc_no = %s,activity_no = %s,清洗数据结束\n" % (ff_acc_no,activity_no))

