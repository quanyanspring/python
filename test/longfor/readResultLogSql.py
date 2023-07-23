import DBConfig as config
import dbutils


def build_sql(params,arr_1):
    print("参数集合为：{}".format(params))
    transaction_id_sql = transaction_id.format(params)
    col_list_m, row_list_m = dbutils.execute_sql(transaction_id_sql, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        print("返回集合数量：{}".format(len(row_list_m)))
        file = open("/Users/admin/Desktop/insert_activity_result_log_01.sql", mode="a", encoding="utf-8")
        arr = []
        arr_3 = []
        for idex, itsm in enumerate(row_list_m):
            arr.append(insert_company_transaction + "values(" + str(itsm).replace("[","").replace("]","").replace("None","null") + ");\n")
            arr_3.append(itsm[2])

        l = list(set(arr_1) - set(arr_3))
        for index,itsm in enumerate(l):
            print("差数据" + itsm)

        file.writelines(arr)
        file.close()



if __name__ == "__main__":
    db_info = config.db_list_info[0]

    transaction_id = """
            select t2.batch_no batch_no,
                   'CZFF_000000001' serial_number,
                   t1.out_trans_no trans_no,
                   t.out_acc_no trans_out,
                   t3.acc_no trans_in,
                   t2.longball_amt trans_amt,
                   'business_type' type_code,
                   t1.business_type code,
                   1 status,
                   t2.create_time create_time,
                   '发放成功_补流水' remark,
                   t1.biz_sys_id biz_sys_id,
                   t.user_id person_id,
                   t4.company_no company_no,
                   t4.acc_name company_name,
                   0 trans_type
            from t_activity_detail_prehandle t2
                     left join t_company_transaction t1 on t2.trans_no = t1.out_trans_no
                     left join t_grant_record t on t2.trans_no = t.request_no
                     left join lf_account t3 on t.user_id = t3.user_id and t.account_type = t3.account_type
                     left join t_account_ff t4 on t.out_acc_no = t4.acc_no
            WHERE t.request_no IN {0}
              and t1.acc_no like 'JS%'
        """

    insert_company_transaction = "insert into t_activity_result_log(batch_no,serial_number,trans_no,trans_out,trans_in,trans_amt,type_code,code,status,create_time,remark,biz_sys_id,person_id,company_no,company_name,trans_type) "



    file = open("/Users/admin/Desktop/export_result_01.txt", mode="r", encoding="utf-8")
    readlines = file.readlines()
    arr = []
    arr_1 = []
    trans_no_list = ""
    set_1 = set(readlines)
    for index,item in enumerate(set_1):
        arr.append("'" + str(item).split(",")[0].replace("'", "") + "'")
        arr_1.append(str(item).split(",")[0].replace("'", ""))

        trans_no_list = ",".join(arr)
        if index%1000 == 0 or index == len(set_1)-1:
            build_sql("(" + trans_no_list + ")",arr_1)
            trans_no_list = ""
            arr = []
            arr_1 = []


