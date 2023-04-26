
import dbutils
import json
import dbutils_prod as dbutils_prod
import requests

server = "http://127.0.0.1:8066/queryOrderNo"

def getExtra(activity_no):
    return '{"activity_no":"%s","source":"platform_grant"}' % activity_no

def post_lmarketing(params):
    data = {
        "list": params
    }
    head = {
        "Content-Type": "application/json"
    }

    return invoke_post(server, head, data)


# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=json.dumps(params), timeout=1000, headers=head)
    if resp.text is not None and resp.text != '[]':
        print("大会员活动流水,活动编号票响应:{%s}" % resp.text)
    return resp.text

def checkFromLmarketing(trans_no_list):
    # 查询大会员
    lmarketing = post_lmarketing(trans_no_list)
    if lmarketing is not None and len(lmarketing) > 0:
        if len(lmarketing) != len(trans_no_list):
            print("查询流水号:%.1f,结果流水号:%.1f" % (len(trans_no_list), len(lmarketing),))
            return
        for itsm in lmarketing:
            order_no = itsm["orderNo"]
            if order_no not in trans_no_list:
                print()
            print()
    trans_no_list.clear()

def updateExtra():
    query_extra_sql = """
            select * from t_company_transaction_tmp where acc_no = 'FF-210910-27129' and target_acc_no regexp 'XF|SH|YH|GLZ' and is_deleted = 0 and `status` = 1 and trans_type = 1 and extra is null limit 1000;
        """

    query_id_sql = """
            select extra from t_company_transaction where out_trans_no = {0} and acc_no = 'FF-210910-27129'
        """
    col_list_m, row_list_c = dbutils.execute_sql(query_extra_sql, "生成trans_no")
    if row_list_c is None or len(row_list_c) < 1:
        print("生成trans_no,错误")
        raise TypeError
    else:
        for index, item in enumerate(row_list_c):
            original_no = item[5]
            out_trans_no = item[4]
            id = item[0]
            if len(original_no) < 0:
                raise ValueError

            # 查询原单活动
            col_list_m, row_list_d = dbutils.execute_sql(query_id_sql.format("'" + original_no + "'"), "生成trans_no")
            if row_list_d is None or len(row_list_d) < 1:
                print("生成trans_no,错误")
                raise TypeError
            else:
                extra = row_list_d[0][0]
                if len(extra) < 1:
                    print("out_trans_no = %s,原始流水无活动编号" % out_trans_no)
                    continue

                activity_no = json.loads(str(extra).replace("\\", ""))["activity_no"]

                update_data = {
                    "data": {
                        "id": id,
                        "extra": getExtra(activity_no)
                    }
                }
                print(update_data)
                # 3、调用接口清洗数据
                dbutils_prod.execute("/api/migrate/modify/com/trans/data", update_data)

if __name__ == "__main__":
    # updateExtra()

    trans_no_list = [
        '001117842442274710259572942',
        '002112050342274761799188675',
        '002112050342274761799188674',
        '007956383714918929679917064',
        '003549229814919238917570565',
        '001117842442274710259572941',
        '002112050342274761799188673',
        '009475192442274710259572847',
        '001097512471400532761223183',
        '008365143983807379019404108',
        '002182928783807396199274666',
        '007005334183835365026291715',
        '005370795883850706649481247',
        '001097802742274761799188625',
        '001535446583805815651299132',
        '005370788783808401221630522',
        '001117842442274710259572945',
        '002112050342274761799188678',
        '009475192442274710259572848',
        '001097512471400541351157760',
        '005370795883850706649481248',
        '001535446583805815651299137',
        '005370788783808401221630523',
        '002182928783807396199274667',
        '008365143983807379019404109',
        '001117842442274710259572944',
        '002112050342274761799188677',
        '001535446583805815651299136',
        '007956383714918929679917066',
        '007956383714918929679917068',
        '003549229814919238917570567',
        '003549229814920596127244294',
        '001117842442274710259572943',
        '002112050342274761799188676',
        '001535446583805815651299133',
        '007956383714918929679917065',
        '007956383714918929679917067',
        '003549229814919238917570566'
    ]

    ff_trans_no_list = [
        '001097512442274710259572884',
        '001097512442274761799188615',
        '001097802742274761799188612',
        '008365143942277656607154257',
        '008365143942274761799188551',
        '001117842442274710259572937',
        '001117842442274761799188667',
        '001117842442274761799188666',
        '001117842442277656607154384',
        '001117842442274761799188665',
        '002112050342274710259572938',
        '002112050342274761799188669',
        '002112050342277656607154386',
        '002112050342274761799188668',
        '002112050342274710259572939',
        '002112050342277656607154385',
        '002182928742277656607154345',
        '002182928742277656607154344',
        '009475192442277656607154251',
        '009475192442274761799188544',
        '007956383714918929679917060',
        '007956383714919238917570561',
        '007956383714918929679917057',
        '007956383714918929679917061',
        '007956383714919238917570562',
        '003549229814918929679917058',
        '003549229814920596127244289',
        '003549229814920596127244288',
        '003549229814919238917570560',
        '007005334142277656607154249',
        '005370795842277656607154258',
        '005370795842274761799188552',
        '001535446542274710259572800',
        '001535446542274710259572801',
        '001535446542277656607154248',
        '001535446542277656607154247',
        '005370788742274761799188516',
        '005370788742274710259572776'
    ]

    checkFromLmarketing(ff_trans_no_list)




