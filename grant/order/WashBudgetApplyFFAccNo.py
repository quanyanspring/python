from test.longfor import dbutils
import dbutils_prod

if __name__ == "__main__":

    id_acc_map = {
        293: "FF-201010-02592",
        2133: "FF-210415-06303",
        2814: "FF-210105-03745",
        2820: "FF-210618-08682",
        415: "FF-201112-03173",
        579: "FF-210125-04453",
        578: "FF-210125-04454",
        577: "FF-210125-04456",
        2395: "FF-210517-07572",
        2363: "FF-210428-07366",
        2386: "FF-210524-07753",
        2385: "FF-210524-07753",
        3824: "FF-210818-11291"
    }

    for k,v in id_acc_map.items():

        params = {
            "id": k,
            "grantAccNo": v
        }
        dbutils_prod.execute("/api/wash/order/budget/apply", params)

    # 查询发放账户为空活动
    apply_sql = """
        SELECT a.activity_no,a.fk_preuse_id,a.id as activity_no_id,a.apply_amount,t.* from t_platform_grant_budget_apply a 
        left join t_company_transaction t on a.fk_preuse_id = t.serial_number
        where a.fk_preuse_id is not null and ( a.grant_acc_no  is null or a.grant_acc_no = '' )
    """

    col_list_m, row_list_m = dbutils.execute_sql(apply_sql, "查询流水")
    if row_list_m is None or len(row_list_m) == 0:
        print("数据为空")
    else:
        for index, item in enumerate(row_list_m):
            activity_no = item[0]
            fk_preuse_id = item[1]
            id = item[2]
            apply_amount = item[3]
            ff_acc_no = item[5]
            trans_amt = item[12]
            trans_type = item[15]
            status = item[16]
            deleted = item[23]
            if status != 1 or deleted == 1:
                print(item)
                continue
            if trans_type != 1:
                print("充值类型错误,{0}".format(str(item)))
                continue
            if apply_amount != trans_amt:
                print("充值金额错误,{0}".format(str(item)))
                continue

            params = {
                "id": id,
                "grantAccNo": ff_acc_no
            }
            dbutils_prod.execute("/api/wash/order/budget/apply", params)
