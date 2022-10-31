import DBConfig as config
import dbutils
import constants
import datetime


def select_sql(sql):
    col_list_m, row_list_m = dbutils.execute_sql(sql, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        print("返回集合数量：{}".format(len(row_list_m)))

        arr_3 = []
        for idex, itsm in enumerate(row_list_m):
            arr_3.append(str(itsm[0]) + "\n")
        file = open("/Users/admin/Desktop/result_04.txt", mode="a", encoding="utf-8")
        file.writelines(arr_3)
        file.close()


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    file = open("/Users/admin/Desktop/20220719-2.txt", mode="r", encoding="utf-8")
    readlines = file.readlines()

    for index, item in enumerate(readlines):
        select_sql(item)
