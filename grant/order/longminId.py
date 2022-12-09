import pandas as pd
import dbutils
import strutils
import os


def writeToExcel(result,sheet_name):
    file_name = "/Users/admin/Desktop/订单模块排查/补充员工OA（新）.xlsx"

    df = pd.DataFrame(result)
    if not os.path.exists(file_name):
        # 写入数据
        with pd.ExcelWriter(file_name) as write:
            df.to_excel(write, sheet_name, index=False,encoding="utf8")
            write.save()
    else:
        # 写入数据
        with pd.ExcelWriter(file_name,mode="a") as write:
            df.to_excel(write, sheet_name, index=False, encoding="utf8")

if __name__ == "__main__":
    excel = pd.read_excel("/Users/admin/Downloads/请补充员工OA.xlsx", sheet_name="Sheet1")
    ncols = excel.shape[0]

    ff_acc_no_map = dict()
    longmin_id_list = []
    index = ncols
    longmin_id_sql = "select account_no,longmin_id from t_account_desensitization where longmin_id in ({0})"
    result_map = dict()
    longmin_id_list_list = []
    account_no_list = []
    for iCol in range(ncols):
        index -= 1
        longmin_id = excel.iloc[iCol, 0]
        longmin_id_list.append("'" + str(longmin_id) + "'")
        if len(longmin_id_list) % 1000 == 0 or index == 81260:
            col_list_m, row_list_m = dbutils.execute_sql(longmin_id_sql.format(",".join(longmin_id_list)), "查询流水")
            if row_list_m is None or len(row_list_m) == 0:
                print("数据为空:%s" % str(longmin_id_list))
            else:
                for index, item in enumerate(row_list_m):
                    longmin_id_list_list.append(item[1])
                    account_no_list.append(item[0])
            longmin_id_list = []



    result_map["龙民id"] = longmin_id_list_list
    result_map["员工OA"] = account_no_list

    writeToExcel(result_map, "sheet1")
