import dbutils_prod as dbutils_prod
from test.longfor import strutils, dbutils
import WashGrantOrderSql as order_sql
from ConstansList import activity_no_map

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
        col_list_m, row_list_c = dbutils.execute_sql(order_sql.t_company_transaction_sql.format("'" + ff_acc_no + "'", strutils.remove_bracket(row_list_g)), "查询项目公司流水id")
        if row_list_c is None or len(row_list_c) <= 0:
            print("发放账户,ff_acc_no = %s,activity_no = %s,无项目公司流水" % (ff_acc_no, activity_no))
            raise RuntimeError
        else:
            if len(row_list_g) != len(row_list_c):
                raise TypeError
            for index, item in enumerate(row_list_c):
                update_data = {
                    "data": {
                        "id": item[0],
                        "extra": getExtra(activity_no)
                    }
                }

                #3、调用接口清洗数据
                dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)

                print("数据清洗成功:{0}".format(update_data))


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

    id_list = [
        269631088,
        269631091,
        269631095,
        269653304,
        269653309,
        269659465,
        269659471,
        269659475,
        269659668
    ]

    ##TODO
    for id in id_list:
        update_data = {
            "data": {
                "id": id,
                "extra": "{\"activity_no\":\"YH2209201340CJ35401\",\"source\":\"platform_grant\"}"
            }
        }
        # 3、调用接口清洗数据
        dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)

    # 循环处理数据
    for activity_no,ff_acc_no in activity_no_map.items():

        print("发放账户,ff_acc_no = %s,activity_no = %s,清洗数据开始" % (ff_acc_no,activity_no))

        #1、清洗数据
        grantListToCompanyTransaction(ff_acc_no,activity_no)
        #2、确认数据
        checkActivity(ff_acc_no,activity_no)

        print("发放账户,ff_acc_no = %s,activity_no = %s,清洗数据结束\n" % (ff_acc_no,activity_no))
        # 插入grant_list数据，手动调帐导致 YG2011200932CJ67301

