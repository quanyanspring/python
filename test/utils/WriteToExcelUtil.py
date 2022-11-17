import os

import pandas
import pandas as pd

def writeToExcel(result,sheet_name,file_name = "流水缺失发放编号详情_checked"):
    file_name = "/Users/admin/Desktop/订单模块排查/%s.xlsx" % file_name

    df = pd.DataFrame(result)
    if not os.path.exists(file_name):
        # 写入数据
        with pandas.ExcelWriter(file_name) as write:
            df.to_excel(write, sheet_name, index=False,encoding="utf8")
            write.save()
    else:
        # 写入数据
        with pandas.ExcelWriter(file_name,mode="a") as write:
            df.to_excel(write, sheet_name, index=False, encoding="utf8")
            write.save()