import dbutils_uat
from test.longfor import TestDBConfig as config, dbutils_UAT as dbutils

if __name__ == "__main__":

    info = config.db_list_info

    #查询发放账户为空活动
    apply_sql = """
        select *
        from t_btrade_order
        where trans_type in (4, 15)
          and in_acc_no_type = 20
          and status = 1
          and serial_no in
              (select fk_preuse_id from t_platform_grant_budget_apply where is_deleted = 0 and fk_preuse_id is not NULL and fk_preuse_id != '' and grant_acc_no is null )
        order by in_acc_no
    """

    bugget_sql = """
        select id,fk_preuse_id,grant_acc_no,apply_amount from t_platform_grant_budget_apply where is_deleted = 0 and fk_preuse_id = {0}
    """

    row_list_m = dbutils.execute_select_sql_uat(apply_sql, info[1])
    if row_list_m is None or len(row_list_m) == 0:
        print("数据为空")
    else:
        for index,item in enumerate(row_list_m):
            serial_no =  item[16]
            ff_acc_no =  item[7]
            amount =  item[10]
            ## 查询是否已经存在
            row_list_m = dbutils.execute_select_sql_uat(bugget_sql.format("'" + serial_no + "'"), info[1])
            if row_list_m is None or len(row_list_m) < 1:
                print("serial_no=%s,ff_acc_no=%s，无数据" % (serial_no, ff_acc_no))
            else:
                row = row_list_m[0]
                if row[2] == ff_acc_no:
                    print("数据已经绑定，serial_no：%s,ff_acc_no:%s" % (serial_no,ff_acc_no))
                # elif row[3] != amount:
                #     print("申请金额和充值金额不一致，serial_no：%s,ff_acc_no:%s,apply_amount:%d,amount:%d" % (serial_no, ff_acc_no, row[3], amount))
                else:
                    params = {
                        "id":row[0],
                        "grantAccNo":ff_acc_no
                    }
                    dbutils_uat.execute("/api/wash/order/budget/apply",params)

