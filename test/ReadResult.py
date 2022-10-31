import json
import pandas as pd

import xlwt

if __name__ == "__main__":

    # 读数据
    excel = pd.read_excel("/Users/admin/Desktop/export_result.xlsx")
    df = excel[["activityNo", "activityStatus", "grantMethod"]]
    activity_no_map = dict()
    index = 0
    for item in df["activityNo"]:
        activity_no_map[item] = [df["activityStatus"][index],df["grantMethod"][index]]
        index += 1

    #写数据
    # activity_no_list = []
    activity_status_list = []
    grant_method_list = []
    data = pd.read_excel("/Users/admin/Desktop/订单模块排查/活动维度排查结果.xlsx",sheet_name="涉及年末清零活动账户（9.7）")
    for item in data["活动编号"]:
        # activity_no_list.append(item)
        if activity_no_map.__contains__(item):
            value = activity_no_map[item]
            activity_status_list.append(value[0])
            grant_method_list.append(value[1])
        else:
            activity_status_list.append("-")
            grant_method_list.append("-")

    # data.insert(2,"activityNo",activity_status_list)
    data.insert(3,"activityStatus",activity_status_list)
    data.insert(4,"grantMethod",grant_method_list)

    frame = pd.DataFrame(data)
    # frame.to_excel("/Users/admin/Desktop/订单模块排查/活动维度排查结果_5的副本.xlsx",sheet_name="初步排查正常账户",index=False)

    with pd.ExcelWriter("/Users/admin/Desktop/订单模块排查/活动维度排查结果.xlsx",mode="a") as write:
        frame.to_excel(write, sheet_name="涉及年末清零活动账户(9.7.1)", index=False, encoding="utf8")
        write.save()

    print("保存完毕")








    if 1==1:
        raise Exception


    example = pd.DataFrame(
        {"Month": ['Jan', 'Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar', 'Mar', 'Mar'],
         "Category": ['Transportation', 'Grocery', 'Household', 'entertainment',
                      'Transportation', 'Grocery', 'Household', 'entertainment',
                      'Transportation', 'Grocery', 'Household', 'entertainment'],
         "Amount": [74, 235, 175, 100, 115, 240, 225, 125, 90, 260, 200, 120]})

    example_poivt = example.pivot(index="Category", columns="Month", values="Amount")

    print(example)
    print(example_poivt)
    print(example_poivt.sum(axis=0))

    ff_acc_no_map = dict()

    with open("/Users/admin/Desktop/订单模块排查/ff_acc_no_result.json", mode="r", encoding="utf-8") as read:
        _acc_no = ""
        _item_list = []
        for item in read.readlines():
            if item.__contains__(",开始"):
                _acc_no = item.split(":")[1].split(",")[0]
                _item_list = []

            elif item.__contains__(",结束"):
                _acc_no = item.split(":")[1].split(",")[0]
                ff_acc_no_map[_acc_no] = _item_list

                _acc_no = ""
            elif len(item) == 1:
                pass
            else:
                _item_list.append(item.replace("\n", "").replace("\"", "").replace("'", "") + ";")

    # 写入excel文件

    result_list = []
    flag = False
    flag_1 = False
    result_map = dict()
    ff_acc_list = []
    value_list = []
    for k, v in ff_acc_no_map.items():
        for item in v:
            if item.__contains__("定时任务-年末余额收回"):
                flag = True
            if item.__contains__("充值-发放-余额-回充,结果不符"):
                flag_1 = True
        if not flag and flag_1:
            ff_acc_list.append(k)
            value_list.append(str(v).replace("[", "").replace("]", "").replace("', '", "\r").replace("'", ""))

        flag = False
        flag_1 = False

    result_map["发放账户"] = ff_acc_list
    result_map["详情"] = value_list

    read.close()
    df = pd.DataFrame(result_map)
    df.to_excel("/Users/admin/Desktop/订单模块排查/初步问题账户.xlsx", "初步问题账户", index=False)
