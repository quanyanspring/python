import datetime

import constants
import dbutils
import dbutils_uat as dbutils_uat
import dbutils_prod as dbutils_prod
from ConstansList import grant_clear_activity_no_map
from datetime import datetime
import Sequence as sequence


def createTroNo():
    create_tro_no_sql = """
        select concat(replace(current_timestamp(3)+0,'.',''),substring(convert(rand(),char),3,5))
    """

    col_list_m, row_list_c = dbutils.execute_sql(create_tro_no_sql, "生成trans_no")
    if row_list_c is None or len(row_list_c) != 1:
        print("生成trans_no,错误")
        raise TypeError
    else:
        return row_list_c[0][0]


if __name__ == "__main__":


    # # 删除 t_platform_grant_clear
    # params = {
    #     "id": 11,
    #     "isDeleted": 1
    # }
    #
    # dbutils_prod.execute("/api/wash/order/grant/clear", params)

    # # 删除 t_account_ff_clear_transaction
    # params = {
    #     "id": 188,
    #     "clearAmt": 13
    # }
    #
    # dbutils_prod.execute("/api/wash/order/ff/clear", params)

    # 循环处理数据
    for activity_no, amount in grant_clear_activity_no_map.items():
        print("活动编号,activity_no = %s,金额:%.1f,清洗数据开始" % (activity_no, amount))

        now_tiime = datetime.now()

        params = {
            "clearType": 1,
            "createTime": now_tiime.strftime(constants.date_time_format),
            "activityNo": activity_no,
            "transNo": sequence.createTroNo(),
            "clearAmt": amount,
            "isDeleted": 0
        }

        # 3、请求insert接口
        dbutils_prod.execute("/api/wash/order/grant/clear", params)

        print("活动编号,activity_no = %s,金额:%.1f,清洗数据结束" % (activity_no, amount))
