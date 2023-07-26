import requests
import json
import pandas as pd
import os

list_server = "http://yapi.longfor.com/api/interface/list?page={0}&limit={1}&project_id=8799"
list_cat_server = "http://yapi.longfor.com/api/interface/list_cat?page=1&limit=20&catid={0}"
del_cat_server = "http://yapi.longfor.com/api/interface/del_cat"
del_server = "http://yapi.longfor.com/api/interface/del"
list_menu_server = "http://yapi.longfor.com/api/interface/list_menu?project_id=8799"
up_server = "http://yapi.longfor.com/api/interface/up"

def read_excel(path,sheetName):

    excel = pd.read_excel(path, sheet_name=sheetName)
    ncols = excel.shape[0]

    path_list = []
    for iCol in range(ncols):
        path = str(excel.iloc[iCol,0])
        path_list.append(path)

    return path_list

def read_source_excel(path,sheetName):

    excel = pd.read_excel(path, sheet_name=sheetName)
    ncols = excel.shape[0]

    path_id_map = {}
    for iCol in range(ncols):
        path_id_map[excel.iloc[iCol,1]] = str(excel.iloc[iCol,0])

    return path_id_map


def wash_excel():

    excel = pd.read_excel("/Users/admin/Desktop/大会员珑珠API Key.xlsx", sheet_name="Sheet1")
    ncols = excel.shape[0]

    path_list = []
    for iCol in range(ncols):
        path = str(excel.iloc[iCol,0])
        if not path.startswith("/"):
            print(path)
        elif path.startswith('http'):
            print(path)
        elif len(path) < 1:
            print(path)
        elif len(path) == 1:
            print(path)
        elif path == '没有用这个' or path == '无':
            print(path)
        else:
            path_list.append(path)

    result_map = {}
    result_map["path"] = list(set(path_list))

    writeToExcel(result_map, "sheet3","/Users/admin/Desktop/大会员珑珠API Key.xlsx")

def writeToExcel(result, sheet_name,file_name):

    if file_name is None or len(file_name) == 0:
        file_name = "/Users/admin/Desktop/yapi/消费.xlsx"

    df = pd.DataFrame(result)
    if not os.path.exists(file_name):
        # 写入数据
        with pd.ExcelWriter(file_name) as write:
            df.to_excel(write, sheet_name, index=False, encoding="utf8")
            write.save()
    else:
        # 写入数据
        with pd.ExcelWriter(file_name, mode="a") as write:
            df.to_excel(write, sheet_name, index=False, encoding="utf8")
            write.save()


def invoke_get(url, head, params):
    resp = requests.get(url, timeout=1000, headers=head)
    if resp.text is not None and resp.text != '[]':
        print("yapi响应:{%s}" % resp.text)
    return resp.text


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=json.dumps(params), timeout=1000, headers=head)
    if resp.text is not None and resp.text != '[]':
        print("yapi响应:{%s}" % resp.text)
    return resp.text


def list_cat():

    params = {

    }

    ## 结果集
    result_map = dict()
    id_list = []
    path_list = []
    page = 1
    limit = 20

    while True:
        post = invoke_get(list_server.format(page, limit), getHeard(), params)

        data_list = json.loads(post)['data']['list']

        if data_list is not None and len(data_list) > 0:

            for idx, item in enumerate(data_list):
                id_list.append(item['_id'])
                path_list.append(item['path'])

        if data_list is None or len(data_list) < 1 or len(data_list) < limit:
            break
        else:
            page = page + 1

    result_map["id"] = id_list
    result_map["path"] = path_list

    writeToExcel(result_map, "sheet1","/Users/admin/Desktop/yapi/消费.xlsx")



def getHeard():
    return {
        "Content-Type": "application/json",
        "Cookie": ""
    }


def del_cat(id):
    params = {
        "id": id
    }
    post = invoke_post(del_server, getHeard(), params)

    errmsg = json.loads(post)['errmsg']
    if errmsg != '成功！':
        print("未删除成功{0},{1}".format(id, errmsg))
    else:
        print("删除成功{0},{1}".format(id, errmsg))


def del_cat_empty():
    params = {

    }

    menu = invoke_get(list_menu_server, getHeard(), params)

    menu_list = json.loads(menu)['data']

    #目录列表
    for item in menu_list:
        cat_id = item['_id']
        if cat_id == 160703:
            continue
        else:
            #查询是否有内容
            get = invoke_get(list_cat_server.format(cat_id), getHeard(), params)
            count_ = json.loads(get)['data']['count']
            if count_ == 0:
                #删除该目录
                del_cat_params = {
                    "catid":cat_id
                }
                post = invoke_post(del_cat_server, getHeard(), del_cat_params)


def del_other():
    des_list = read_excel("/Users/admin/Desktop/大会员珑珠API Key.xlsx", "sheet3")
    source_map = read_source_excel("/Users/admin/Desktop/yapi/消费.xlsx", "sheet1")

    in_id_list = []
    in_path_list = []
    out_list = []
    for k, v in source_map.items():
        if des_list.__contains__(k):
            in_id_list.append(v)
            in_path_list.append(k)
        else:
            out_list.append(v)

    ## 删除id
    for item in out_list:
        del_cat(item)

    errot_list = set(des_list) - set(in_path_list)
    print(errot_list)


def up_interface():
    source_map = read_source_excel("/Users/admin/Desktop/yapi/消费.xlsx", "sheet1")

    for k, v in source_map.items():
        params = {
            "id": v,
            "catid": 175911
        }
        post = invoke_post(up_server, getHeard(), params)


if __name__ == "__main__":

    # 查询所有路径
    # list_cat()

    # 删除空目录
    del_cat_empty()

    # 清洗源路径
    # wash_excel()

    # 删除不在源路径中的地址
    # del_other()

    #移动目录
    # up_interface()


