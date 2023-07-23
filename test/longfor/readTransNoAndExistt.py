import DBConfig as config
import dbutils


def select_sql(params,arr_4):
    params_sql_1 = params_sql.format(params)

    col_list_m, row_list_m = dbutils.execute_sql(params_sql_1, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        print("返回集合数量：{}".format(len(row_list_m)))

        arr_3 = []
        for idex, itsm in enumerate(row_list_m):
            arr_3.append(itsm[0])

        l = list(set(arr_4) - set(arr_3))

        if len(l) == 0:
            return

        file = open("/Users/admin/Desktop/export_result_01.txt", mode="a", encoding="utf-8")

        arr_2 = []
        for idex, itsm in enumerate(l):
            arr_2.append("'" + itsm + "'\n")

        file.writelines(arr_2)
        file.close()




if __name__ == "__main__":
    db_info = config.db_list_info[0]

    params_sql = """
        select trans_no from t_activity_result_log where trans_no in {0};
    """

    file = open("/Users/admin/Desktop/insert.txt", mode="r", encoding="utf-8")
    readlines = file.readlines()


    set_1 = set(readlines)
    print("集合数量为：{0}".format(str(len(set_1))))

    arr = []
    arr_4 = []
    trans_no = []
    trans_no_list = ""
    for index,item in enumerate(set_1):
        arr.append("'" + str(item).split(",")[0].replace("'", "") + "'")
        arr_4.append(str(item).split(",")[0].replace("'", ""))

        trans_no_list = ",".join(arr)
        if index%1000 == 0 or index == len(set_1)-1:
            select_sql("(" + trans_no_list + ")",arr_4)

            trans_no_list = ""
            arr = []
            arr_4 = []


