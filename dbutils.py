import datetime
import time
import json
from prettytable import PrettyTable
import requests
from DBConfig import db_list_info

server = "http://dbaexecsql.longfor.com/data_application/app_query/"

def getDbInfo():
    return db_list_info[0]

# 执行sql 并查询
def execute_sql(sql, detail,toJSon = False):

    start_cond = time.time()
    head = {
        "Cookie": "IM_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4ODhlNGNkZC1iNzQyLTQ2NmQtOGIwNS04OGQyMTlmNWFmM2QiLCJpc3MiOiJkcmFnb25sZXR0ZXIzLjAiLCJzdWIiOiJ7XCJ1c2VyTmFtZVwiOlwid2FuZ2xpbnF1YW5cIixcInVzZXJJZFwiOlwiNjAwMDMyOTE5XCJ9IiwiaWF0IjoxNjY5NDc0Mjg0LCJleHAiOjE2Njk1NjA2ODR9.H4hncN5-z4mSece8Bw9MtJPAcaFHnnyfnNCsxGFCIpc; sessionid=vrp7ap3i3a989yowy08iipwg9vloco94; SERVERID=3ac2c09d9a96f6ab9569d368ea723c2c|1669604219|1669604158; rd_pic_tkn=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZWFsTmFtZSI6IueOi-ael-WFqCIsInVzZXJJbmZvIjoie1wicG9ydHJhaXRVcmxcIjpcImh0dHBzOi8vcHJvZC1sb25neGluLW9zcy5vc3MtY24tYmVpamluZy5hbGl5dW5jcy5jb20vb3JpZ2luYWwtbmFzLXByby9oZWFkSW1nezF9NjAwMDMyOTE5LmpwZz9oZWFkSWQ9MTAwMDFcIixcInNleFwiOjEsXCJkZXB0SW5mb1wiOlt7XCJkZXB0c1wiOlt7XCJiaXpJZFwiOlwiMTAwMDAwMDAwM1wiLFwibmFtZVwiOlwi6b6Z5rmW6ZuG5ZuiXCJ9LHtcImJpeklkXCI6XCIxMDAwMDAwMDcxXCIsXCJuYW1lXCI6XCLmlbDnp5Hmmbrog73lvJXmk45cIn0se1wiYml6SWRcIjpcIjYwMDAwNDU2ODhcIixcIm5hbWVcIjpcIueUqOaIt-i_kOiQpeaVsOWtl-WMluS4reW_g1wifSx7XCJiaXpJZFwiOlwiNjAwMDE2OTk1NFwiLFwibmFtZVwiOlwi5oqA5pyv5Zui6ZifXCJ9LHtcImJpeklkXCI6XCI2MDAwMjE0MzQ1XCIsXCJuYW1lXCI6XCLmoLjlv4Pns7vnu5_noJTlj5Hnu4RcIn1dLFwiaXNNYWluXCI6MSxcImpvYlwiOlwi5byA5Y-R5ZGY5belXCJ9XX0iLCJleHBpcmVUaW1lIjoxNjY5NjkwODA4MzUyLCJyb2xlQ29kZSI6IjEiLCJpc3MiOiLnjovmnpflhagiLCJ1c2VySWQiOiJ3YW5nbGlucXVhbiIsImZpbGVJZCI6ImVkYTh3UWI2dkFrcTk4STVFRFM3UGl2bVBBc3IifQ.a7DXKLH1ZPYeL2n8c5F42RUCQMfN78MemrFSdriWZ14; CASTGC=TGT-681740-L9y4Y3Q5WSwo-HZCwTRDZhpllzeaaiUlWKR44uw-t64PZogJfnpJ4y7I-JExHYCQCyc-longhu; account=TGT-681740-L9y4Y3Q5WSwo-HZCwTRDZhpllzeaaiUlWKR44uw-t64PZogJfnpJ4y7I-JExHYCQCyc-longhu",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "dbaexecsql.longfor.com",
        "Origin": "http: // dbaexecsql.longfor.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    # 去除换行
    sql = " ".join(sql.strip().split("\n"))
    # 请求数据
    data = {
        "instance_name": getDbInfo()[1],
        "db_name": getDbInfo()[2],
        "schema_name": "",
        "tb_name": "",
        "sql_content": sql,
        "limit_num": 10000
    }
    # print("start migrate trans ")
    body = invoke_post(server, head, data)
    try:
        json_body = json.loads(body)
    except Exception as e:
        print(sql)
        print(e)
        raise TimeoutError
    cost_time = str((time.time() - start_cond))

    # print(json_body)
    # 处理成功的情况
    if "status" in json_body and "data" in json_body:
        msg = json_body["msg"]
        # print(msg)

        data_cont = json_body["data"]
        if "affected_rows" in data_cont and "query_time" in data_cont:
            # print("结果总数：%d，查询时间：%f" % (data_cont["affected_rows"], data_cont["query_time"]))
            pass

        if "column_list" not in data_cont:
            print("\n" + sql)
            return None, None

        col_list = data_cont["column_list"]
        row_list = data_cont["rows"]
        full_sql = data_cont["full_sql"]
        error = data_cont["error"]
        query_time = data_cont["query_time"]

        if len(row_list) == 0:
            # print(detail + " 校验通过 cost_time " + cost_time)
            return col_list, None
        else:
            pass
            # print("{} execute sql \n{} \ncost time {}\n error {}".format(get_datetime(), full_sql, query_time, error))
            # print(detail + " 校验不通过 cost_time " + cost_time)

        tb = PrettyTable()  # 生成表格对象
        tb.field_names = col_list  # 定义表头

        for nd in row_list:
            tb.add_row(nd)  # 添加一行，列是column

        # print("")
        # print(tb)
        #  print("total line {}".format(len(row_list)))
        result_list = []
        if toJSon:
            for item in row_list:
                if len(item) >= 0:
                    result = {}
                    for idx,value in enumerate(item):
                        if isinstance(value,int):
                            result["\"" + underline2Hump(col_list[idx]) + "\""] = value
                        elif isinstance(value, str) or isinstance(value, float):
                            if col_list[idx] == 'extra':
                                result["\"" + underline2Hump(col_list[idx]) + "\""] = json.dumps(str(value))
                            else:
                                result["\"" + underline2Hump(col_list[idx]) + "\""] = "\"" + str(value) + "\""
                        elif value == None:
                            pass
                        else:
                           result["\"" + underline2Hump(col_list[idx]) + "\""] = value
                    result_list.append(result)

            return col_list,result_list

        return col_list, row_list


def get_datetime():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return date_str


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=params, timeout=1000, headers=head)
    return resp.text


# tidb 数据查询
def execute_tidb_sql(sql, instance="tidb10.31.48.7_脱敏查询", db_name="longem_tidb", detail="query"):
    return execute_sql(sql, detail, instance, db_name)

def underline2Hump(text):
    arr = text.lower().split('_')
    res = []
    for idx,var in enumerate(arr):
        if len(arr) == 1:
            res.append(var)
            break
        elif idx == 0:
            res.append(var)
            continue
        else:
            res.append(var[0].upper() + var[1:])
    return ''.join(res)
