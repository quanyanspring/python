import DBConfig as config
import dbutils


def build_sql(params,arr_1,arr_4):
    print("参数集合为：{}".format(params))
    transaction_id_sql = transaction_id.format(params)
    col_list_m, row_list_m = dbutils.execute_sql(transaction_id_sql, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        print("返回集合数量：{}".format(len(row_list_m)))
        file = open("/Users/admin/Desktop/insert_t_company_transaction.sql", mode="a", encoding="utf-8")
        arr = []
        arr_3 = []
        for idex, itsm in enumerate(row_list_m):
            if arr_4.get(itsm[3]) is not None:
                extra = ",'{\"activity_no\":\"" + arr_4.get(itsm[3]) + "\",\"source\":\"platform_grant\"}'"
                arr.append(insert_company_transaction + "values(" + str(itsm).replace("[", "").replace("]", "").replace("None","null") + extra + ");\n")
            else:
                arr.append(insert_company_transaction + "values(" + str(itsm).replace("[", "").replace("]", "").replace("None", "null")  + ",null);\n")

            arr_3.append(itsm[3])

        l = list(set(arr_1) - set(arr_3))
        for index,itsm in enumerate(l):
            print("差异集合："+ itsm)

        file.writelines(arr)
        file.close()

def select_sql():
    col_list_m, row_list_m = dbutils.execute_sql(params_sql, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        print("返回集合数量：{}".format(len(row_list_m)))
        file = open("/Users/admin/Downloads/export_result2022.txt", mode="r", encoding="utf-8")
        readlines = file.readlines()
        map = {}
        for index,item in enumerate(readlines):
            split = item.split(",")
            map[split[0]] = split[2].replace("\n","")

        arr = []
        for idex, itsm in enumerate(row_list_m):
            sql = "UPDATE t_company_transaction SET extra = '{\"activity_no\":\"" + map[itsm[1]] + "\",\"source\":\"platform_grant\"}' WHERE id =" + str(itsm[0]) + ";"
            print(sql)
            arr.append(sql)




if __name__ == "__main__":
    db_info = config.db_list_info[0]




    update_sql = """
        UPDATE t_company_transaction SET extra = '{"activity_no":" 
    """

    extra = """
                ,'{"activity_no":"{0}","source":"platform_grant"}'
            """


    transaction_id = """
            select t.out_acc_no acc_no,
                   t2.batch_no batch_no,
                   concat(t1.trans_no, "_1")  trans_no,
                   t1.out_trans_no out_trans_no,
                   t3.acc_no target_acc_no,
                   t2.longball_amt trans_amt,
                   t1.business_type business_type,
                   2 trans_type,
                   1 status,
                   now(6) create_time,
                   'system' create_user,
                   now(6) modify_time,
                   0 is_deleted,
                   t1.company_channel company_channel,
                   t1.biz_sys_id biz_sys_id
            from t_activity_detail_prehandle t2
                     left join t_company_transaction t1 on t2.trans_no = t1.out_trans_no
                     left join t_grant_record t on t2.trans_no = t.request_no
                     left join lf_account t3 on t.user_id = t3.user_id and t.account_type = t3.account_type
            where t.request_no in {0}
              and t1.acc_no like 'JS%';
        """

    insert_company_transaction = "insert into t_company_transaction(acc_no,batch_no,trans_no,out_trans_no,target_acc_no,trans_amt,business_type,trans_type,status,create_time,create_user,modify_time,is_deleted,company_channel,biz_sys_id,extra)"

    params_sql = """
        SELECT id,out_trans_no,extra from t_company_transaction where extra = '{"source":"platform_grant"}' and id > 208374087
    """

    # select_sql()




    file_1 = open("/Users/admin/Desktop/platform_grant.txt", mode="r", encoding="utf-8")
    file___readlines = file_1.readlines()
    arr_4 = {}
    for index, item in enumerate(file___readlines):
        split = item.split(",")
        arr_4[split[0]] = split[1]



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
            build_sql("(" + trans_no_list + ")",arr_1,arr_4)
            trans_no_list = ""
            arr = []
            arr_1 = []


