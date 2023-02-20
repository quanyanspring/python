import json
import time

import requests

server = "https://api.longhu.net/lf-wallet-endpoint-prod"

# 请求数据
def invoke_post(url, head, params):
    resp = requests.post(url, data=params, timeout=1000, headers=head)
    return resp.text


# 打印到文件
def execute(path, params, type='post'):
    head = {
        "x-gaia-api-key": "edcd2b2c-7174-46a4-9929-09c619087243",
        "x-lc-op-loginkey": "TGT-213567-fvX--r9KnYt6KMThoBfp9c4dV-unbCzkpepxWZ5HIpAYDmJdnFHOSpbgbaTEvgwnUT8-longhu",
        "castgc": "TGT-213567-fvX--r9KnYt6KMThoBfp9c4dV-unbCzkpepxWZ5HIpAYDmJdnFHOSpbgbaTEvgwnUT8-longhu",
        "Content-Type": "application/json"
    }

    params = json.dumps(params)
    print("请求参数:%s", params)

    url = server + path

    if type == 'post':
        body = invoke_post(url, head, params)

    try:
        json_body = json.loads(body)

        if json_body == 1:
            print("insert platform_grant_list数量为：%d" % json_body)

        elif "data" in json_body:
            print("响应结果：%s" % str(json_body))

    except Exception as e:
        print(url)
        print(e)
        raise TimeoutError


if __name__ == "__main__":

    params = {
        "topic": "2023年日常销账",
        "validDateTime": "2023-01-01 00:00:00",
        "accountFfClearActivityTypeReqList": [
            {
                "activityType": "20269",
                "activityName": "短训短调珑珠"
            },
            {
                "activityType": "20110",
                "activityName": "总部乔迁红包"
            },
            {
                "activityType": "20102",
                "activityName": "综合通讯珑珠增发"
            },
            {
                "activityType": "006",
                "activityName": "中秋节礼金"
            },
            {
                "activityType": "20195",
                "activityName": "智慧新材全员营销"
            },
            {
                "activityType": "012",
                "activityName": "职级交通珑珠"
            },
            {
                "activityType": "20068",
                "activityName": "知识竞答激励"
            },
            {
                "activityType": "20002",
                "activityName": "长期服务激励"
            },
            {
                "activityType": "20149",
                "activityName": "云图梭激励"
            },
            {
                "activityType": "20079",
                "activityName": "员工资质激励"
            },
            {
                "activityType": "20080",
                "activityName": "员工培训激励"
            },
            {
                "activityType": "20038",
                "activityName": "员工差旅珑珠"
            },
            {
                "activityType": "20256",
                "activityName": "佑佑营销活动"
            },
            {
                "activityType": "20241",
                "activityName": "佑佑全员营销"
            },
            {
                "activityType": "20257",
                "activityName": "佑佑客户关系维护"
            },
            {
                "activityType": "20215",
                "activityName": "友工有钱运营活动"
            },
            {
                "activityType": "20052",
                "activityName": "友工有钱激励"
            },
            {
                "activityType": "20162",
                "activityName": "异地珑珠"
            },
            {
                "activityType": "20065",
                "activityName": "业主运营活动"
            },
            {
                "activityType": "20081",
                "activityName": "业务达人激励"
            },
            {
                "activityType": "20085",
                "activityName": "养老渠道激励"
            },
            {
                "activityType": "20133",
                "activityName": "养老营销活动"
            },
            {
                "activityType": "20160",
                "activityName": "学习体验珑珠"
            },
            {
                "activityType": "007",
                "activityName": "新婚礼金"
            },
            {
                "activityType": "20197",
                "activityName": "小B拉新激励"
            },
            {
                "activityType": "011",
                "activityName": "团队珑珠"
            },
            {
                "activityType": "20036",
                "activityName": "通讯珑珠"
            },
            {
                "activityType": "20084",
                "activityName": "塘鹅客户关系维护"
            },
            {
                "activityType": "20103",
                "activityName": "塘鹅全员营销"
            },
            {
                "activityType": "20114",
                "activityName": "塘鹅运营活动"
            },
            {
                "activityType": "20115",
                "activityName": "塘鹅美装修全员营销"
            },
            {
                "activityType": "20124",
                "activityName": "塘鹅推荐租房积分"
            },
            {
                "activityType": "20125",
                "activityName": "塘鹅推荐购房积分"
            },
            {
                "activityType": "20126",
                "activityName": "塘鹅购新房积分"
            },
            {
                "activityType": "20127",
                "activityName": "塘鹅租房积分"
            },
            {
                "activityType": "20128",
                "activityName": "塘鹅出租积分"
            },
            {
                "activityType": "20129",
                "activityName": "塘鹅购二手房积分"
            },
            {
                "activityType": "20130",
                "activityName": "塘鹅售二手房积分"
            },
            {
                "activityType": "20221",
                "activityName": "塘鹅营销活动"
            },
            {
                "activityType": "20222",
                "activityName": "塘鹅评优激励"
            },
            {
                "activityType": "20223",
                "activityName": "塘鹅推荐激励"
            },
            {
                "activityType": "20184",
                "activityName": "随机立减"
            },
            {
                "activityType": "002",
                "activityName": "生日礼金"
            },
            {
                "activityType": "20067",
                "activityName": "社群运营激励"
            },
            {
                "activityType": "003",
                "activityName": "入职礼金"
            },
            {
                "activityType": "20164",
                "activityName": "人才活动返珑珠"
            },
            {
                "activityType": "20249",
                "activityName": "千丁全员营销"
            },
            {
                "activityType": "20261",
                "activityName": "千丁员工激励"
            },
            {
                "activityType": "029",
                "activityName": "其他"
            },
            {
                "activityType": "20061",
                "activityName": "品牌公关活动"
            },
            {
                "activityType": "20189",
                "activityName": "品牌运营活动"
            },
            {
                "activityType": "20230",
                "activityName": "品牌传播活动"
            },
            {
                "activityType": "20231",
                "activityName": "品牌IP活动"
            },
            {
                "activityType": "20157",
                "activityName": "膨胀珑珠"
            },
            {
                "activityType": "004",
                "activityName": "女神节礼金"
            },
            {
                "activityType": "20037",
                "activityName": "暖心珑珠（原综合珑珠）"
            },
            {
                "activityType": "20032",
                "activityName": "年会评优奖金"
            },
            {
                "activityType": "048",
                "activityName": "内推激励"
            },
            {
                "activityType": "049",
                "activityName": "珑珠运营激励"
            },
            {
                "activityType": "20208",
                "activityName": "珑珠优选运营活动"
            },
            {
                "activityType": "20233",
                "activityName": "珑珠优选消费积分"
            },
            {
                "activityType": "20112",
                "activityName": "珑珠用户维护"
            },
            {
                "activityType": "20227",
                "activityName": "珑珠券-项目补贴发放"
            },
            {
                "activityType": "20182",
                "activityName": "珑珠客服赔付"
            },
            {
                "activityType": "028",
                "activityName": "龙币转珑珠"
            },
            {
                "activityType": "20165",
                "activityName": "领导力中心推荐激励"
            },
            {
                "activityType": "025",
                "activityName": "快捷支付充值"
            },
            {
                "activityType": "010",
                "activityName": "开工珑珠（员工）"
            },
            {
                "activityType": "009",
                "activityName": "家属礼金"
            },
            {
                "activityType": "20255",
                "activityName": "活动权益积分"
            },
            {
                "activityType": "20202",
                "activityName": "会员分润激励"
            },
            {
                "activityType": "050",
                "activityName": "管理层打赏金"
            },
            {
                "activityType": "038",
                "activityName": "管理层充值"
            },
            {
                "activityType": "20082",
                "activityName": "公车加油金"
            },
            {
                "activityType": "20264",
                "activityName": "工作圈运营"
            },
            {
                "activityType": "013",
                "activityName": "岗位交通珑珠"
            },
            {
                "activityType": "20205",
                "activityName": "发放测试"
            },
            {
                "activityType": "005",
                "activityName": "端午节礼金"
            },
            {
                "activityType": "035",
                "activityName": "调研咨询激励"
            },
            {
                "activityType": "008",
                "activityName": "奠仪金"
            },
            {
                "activityType": "20174",
                "activityName": "成长体验珑珠"
            },
            {
                "activityType": "20076",
                "activityName": "产品测试激励"
            },
            {
                "activityType": "098",
                "activityName": "布草珑珠"
            },
            {
                "activityType": "20116",
                "activityName": "保险全员营销"
            },
            {
                "activityType": "20234",
                "activityName": "保险用户运营"
            },
            {
                "activityType": "20235",
                "activityName": "保险员工激励"
            },
            {
                "activityType": "016",
                "activityName": "榜样的力量激励"
            },
            {
                "activityType": "20070",
                "activityName": "IP门店激励"
            },
            {
                "activityType": "20163",
                "activityName": "IP彩票兑换"
            },
            {
                "activityType": "20087",
                "activityName": "C4地产服务活动"
            },
            {
                "activityType": "20088",
                "activityName": "C4准业主维护"
            },
            {
                "activityType": "20093",
                "activityName": "C4UG全员营销"
            },
            {
                "activityType": "20094",
                "activityName": "C4美居全员营销"
            },
            {
                "activityType": "20095",
                "activityName": "C4社区活动"
            },
            {
                "activityType": "20096",
                "activityName": "C4美居巡检"
            },
            {
                "activityType": "20111",
                "activityName": "C4管家关系维护"
            },
            {
                "activityType": "20122",
                "activityName": "C4缴物业费积分"
            },
            {
                "activityType": "20123",
                "activityName": "C4增值消费积分"
            },
            {
                "activityType": "20135",
                "activityName": "C4拉新激励"
            },
            {
                "activityType": "20145",
                "activityName": "C4UG破亿激励"
            },
            {
                "activityType": "20152",
                "activityName": "C4物业费回收激励"
            },
            {
                "activityType": "20190",
                "activityName": "C4会员运营活动"
            },
            {
                "activityType": "20191",
                "activityName": "C4增值业务运营"
            },
            {
                "activityType": "20192",
                "activityName": "C4物业费调价激励"
            },
            {
                "activityType": "20193",
                "activityName": "C4管家通讯珑珠"
            },
            {
                "activityType": "20211",
                "activityName": "C4客户关系维护"
            },
            {
                "activityType": "20224",
                "activityName": "C4增值全员营销"
            },
            {
                "activityType": "20232",
                "activityName": "C4物业缴费活动"
            },
            {
                "activityType": "20236",
                "activityName": "C4投发推荐激励"
            },
            {
                "activityType": "024",
                "activityName": "C3营销老带新"
            },
            {
                "activityType": "041",
                "activityName": "C3签约激励"
            },
            {
                "activityType": "20119",
                "activityName": "C3新签积分"
            },
            {
                "activityType": "20120",
                "activityName": "C3续租积分"
            },
            {
                "activityType": "20121",
                "activityName": "C3推荐积分"
            },
            {
                "activityType": "20176",
                "activityName": "C3运营活动"
            },
            {
                "activityType": "20237",
                "activityName": "C3老带新积分"
            },
            {
                "activityType": "20238",
                "activityName": "C3新带新积分"
            },
            {
                "activityType": "20260",
                "activityName": "C3产城推荐积分"
            },
            {
                "activityType": "046",
                "activityName": "C2拉新激励"
            },
            {
                "activityType": "047",
                "activityName": "C2商业分销返佣"
            },
            {
                "activityType": "096",
                "activityName": "C2会员消费积分"
            },
            {
                "activityType": "097",
                "activityName": "C2会员营销积分"
            },
            {
                "activityType": "20077",
                "activityName": "C2消费者激励"
            },
            {
                "activityType": "20078",
                "activityName": "C2商户激励"
            },
            {
                "activityType": "20083",
                "activityName": "C2会员评价激励"
            },
            {
                "activityType": "001",
                "activityName": "C1营销老带新"
            },
            {
                "activityType": "027",
                "activityName": "C1运营赔付"
            },
            {
                "activityType": "037",
                "activityName": "C1客关描摹激励"
            },
            {
                "activityType": "20060",
                "activityName": "C1全员营销"
            },
            {
                "activityType": "20063",
                "activityName": "C1营销商机激励"
            },
            {
                "activityType": "20075",
                "activityName": "C1供方会员激励"
            },
            {
                "activityType": "20089",
                "activityName": "C1营销实习生激励"
            },
            {
                "activityType": "20104",
                "activityName": "C1营销线上活动"
            },
            {
                "activityType": "20117",
                "activityName": "C1签约积分"
            },
            {
                "activityType": "20118",
                "activityName": "C1推荐积分"
            },
            {
                "activityType": "20131",
                "activityName": "C1营销线下活动"
            },
            {
                "activityType": "20151",
                "activityName": "C1签约折扣"
            },
            {
                "activityType": "20258",
                "activityName": "C1营销流量运营"
            }
        ],
        "accountFfClearWhiteListReqList": [
            {
                "accNo": "FF-221223-45116",
                "accName": "重庆珑珠信息科技有限公司-珑珠运营激励-年末专用-014"
            },
            {
                "accNo": "FF-221228-45146",
                "accName": "苏州首龙置业有限公司-商运-C2招商答谢活动-013"
            },
            {
                "accNo": "FF-221227-01220",
                "accName": "北京仟万间科技有限公司-塘鹅拉新激励-154"
            },
            {
                "accNo": "FF-210824-11830",
                "accName": "重庆珑珠信息科技有限公司-C5拉新激励-014"
            },
            {
                "accNo": "FF-211115-39541",
                "accName": "青岛仟万间塘鹅房产有限公司-C5拉新激励-014"
            },
            {
                "accNo": "FF-220322-43090",
                "accName": "成都仟万间塘鹅房产租售有限公司-C5拉新激励-154"
            },
            {
                "accNo": "FF-220407-43302",
                "accName": "青岛仟万间塘鹅房产有限公司-C5拉新激励-154"
            },
            {
                "accNo": "FF-210513-07542",
                "accName": "龙湖物业服务集团有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210520-07689",
                "accName": "龙湖物业服务集团有限公司济南分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210527-08107",
                "accName": "龙湖物业服务集团有限公司苏州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210603-08263",
                "accName": "福州龙湖物业服务有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210611-08397",
                "accName": "龙湖物业服务集团有限公司上海分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210611-08409",
                "accName": "龙湖物业服务集团有限公司中山分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210611-08410",
                "accName": "广州龙湖物业服务有限公司珠海分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210616-08629",
                "accName": "龙湖物业服务集团有限公司广州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210618-08693",
                "accName": "成都龙湖物业服务有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210621-08726",
                "accName": "龙湖物业服务集团有限公司晋江分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210627-08791",
                "accName": "龙湖物业服务集团有限公司福州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210629-08836",
                "accName": "龙湖物业服务集团有限公司合肥分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210707-08958",
                "accName": "成都龙湖物业服务有限公司新津分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210715-09102",
                "accName": "贵阳龙湖物业服务有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210720-09321",
                "accName": "济南龙湖泰熙房地产开发有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210720-09338",
                "accName": "成都辰启置业有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210727-09575",
                "accName": "成都龙湖物业服务有限公司郫县分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210810-11099",
                "accName": "龙湖物业服务集团有限公司长沙分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210915-27971",
                "accName": "龙湖物业服务集团有限公司徐州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-210924-29085",
                "accName": "龙湖物业服务集团有限公司常州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-211207-40250",
                "accName": "龙湖物业服务集团有限公司南京分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-211209-40299",
                "accName": "无锡龙湖物业服务有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-211211-40331",
                "accName": "常州龙湖物业管理有限公司-C4工开交付-014"
            },
            {
                "accNo": "FF-211219-40495",
                "accName": "厦门龙湖物业服务有限公司漳州分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-220226-42603",
                "accName": "贵阳龙湖物业服务有限公司云岩分公司-C4工开交付-014"
            },
            {
                "accNo": "FF-220329-43167",
                "accName": "龙湖物业服务集团有限公司天津分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220429-43565",
                "accName": "成都龙湖物业服务有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220429-43566",
                "accName": "成都龙湖物业服务有限公司新津分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220430-43571",
                "accName": "龙湖物业服务集团有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220527-43890",
                "accName": "贵阳龙湖物业服务有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220613-44007",
                "accName": "福州龙湖物业服务有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220616-44024",
                "accName": "西安龙湖物业服务有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220617-44040",
                "accName": "龙湖物业服务集团有限公司佛山分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220621-44063",
                "accName": "西安龙湖地产发展有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220624-44080",
                "accName": "龙湖物业服务集团有限公司厦门分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220715-44170",
                "accName": "龙湖物业服务集团有限公司合肥分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220913-44539",
                "accName": "龙湖物业服务集团有限公司中山分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220916-44568",
                "accName": "厦门龙湖物业服务有限公司泉州台商投资区分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-220917-44573",
                "accName": "北京龙湖物业服务有限公司唐山分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-221116-44870",
                "accName": "龙湖物业服务集团有限公司昆明分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-221221-45102",
                "accName": "厦门龙湖物业服务有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-221223-45114",
                "accName": "龙湖物业服务集团有限公司南京分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-221228-45145",
                "accName": "广州龙湖物业服务有限公司珠海分公司-C4工开交付-019"
            },
            {
                "accNo": "FF-221230-45171",
                "accName": "云南宜置置业有限公司-C4工开交付-019"
            },
            {
                "accNo": "FF-201224-03593",
                "accName": "北京集顺工程咨询有限公司-C1客关即时评价-014"
            },
            {
                "accNo": "FF-210626-08786",
                "accName": "北京龙智工程咨询有限公司-C1客关即时评价-014"
            },
            {
                "accNo": "FF-220517-43772",
                "accName": "北京龙智工程咨询有限公司-C1客关即时评价-019"
            },
            {
                "accNo": "FF-200924-02102",
                "accName": "合肥锦瑶房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210225-05566",
                "accName": "宁波龙禧房地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210227-05574",
                "accName": "沈阳龙湖新北置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210309-06007",
                "accName": "无锡嘉睿置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210310-06033",
                "accName": "南京名盛置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210312-06049",
                "accName": "西安传化盛世地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210317-06088",
                "accName": "沈阳恒嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210318-06096",
                "accName": "合肥锦东房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210319-06099",
                "accName": "烟台龙湖置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210321-06108",
                "accName": "大连恒瑞房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210323-06117",
                "accName": "南京金名城置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210324-06120",
                "accName": "南京名辰置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210324-06121",
                "accName": "咸阳龙湖彩虹置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210408-06240",
                "accName": "济南泰捷房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210408-06246",
                "accName": "成都龙湖辰顺置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210414-06290",
                "accName": "成都中鼎绿舟置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210414-06292",
                "accName": "青岛龙逸置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210414-06293",
                "accName": "成都辰启置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210414-06301",
                "accName": "成都龙湖辰治置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210416-07284",
                "accName": "成都辰华置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210419-07298",
                "accName": "合肥锦皖源房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210419-07299",
                "accName": "无锡市嘉安置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210419-07300",
                "accName": "成都龙湖西城置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210420-07311",
                "accName": "济南龙湖泰朗房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210421-07328",
                "accName": "郑州龙祥房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210421-07330",
                "accName": "重庆龙湖地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210422-07340",
                "accName": "济南龙湖泰熙房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210423-07341",
                "accName": "无锡嘉腾置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210425-07350",
                "accName": "南通礴麒房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210507-07462",
                "accName": "宁波龙耀房地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210507-07463",
                "accName": "宁波龙湖置业发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210510-07513",
                "accName": "武汉园博园置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210512-07524",
                "accName": "桐乡市安宇置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210514-07547",
                "accName": "合肥锦河房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210514-07548",
                "accName": "杭州龙郦实业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210517-07564",
                "accName": "南宁金泓盛房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210518-07574",
                "accName": "上海湖鑫房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210519-07660",
                "accName": "南宁市渝银实业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210520-07675",
                "accName": "武汉尚龙置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210520-07679",
                "accName": "成都辰敏置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210521-07699",
                "accName": "大连龙湖泽迎置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210521-07717",
                "accName": "南宁龙湖卓景置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210525-08057",
                "accName": "长沙龙湖房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210527-08102",
                "accName": "武汉安和盛泰房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210527-08110",
                "accName": "宁波龙兆房地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210528-08161",
                "accName": "茂名市嘉逊置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210529-08169",
                "accName": "福州盛元房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210602-08247",
                "accName": "南宁龙湖金耀置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210602-08252",
                "accName": "重庆龙湖宜祥地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210603-08269",
                "accName": "大连华昱置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210608-08327",
                "accName": "青岛龙湖置业拓展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210609-08345",
                "accName": "南京市颐辉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210609-08349",
                "accName": "武汉龙嘉房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210609-08350",
                "accName": "武汉市鑫呈捷房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210609-08351",
                "accName": "武汉文泓置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210609-08357",
                "accName": "武汉清龙置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210610-08382",
                "accName": "湖南映客置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210615-08601",
                "accName": "常德龙柳置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210615-08608",
                "accName": "威海市金猴置地有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210617-08646",
                "accName": "天津睿阳置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210618-08701",
                "accName": "济南泰晖房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210618-08702",
                "accName": "重庆龙湖创佑地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210619-08705",
                "accName": "济南安齐房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210619-08708",
                "accName": "河北龙湖亿城房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210623-08750",
                "accName": "武汉晨鸣中利置业有限责任公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210623-08752",
                "accName": "重庆龙湖朗骏房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210624-08755",
                "accName": "厦门龙湖德嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210625-08769",
                "accName": "江西龙湖地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210626-08779",
                "accName": "石狮龙湖恒嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210626-08780",
                "accName": "晋江龙湖晋嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210627-08787",
                "accName": "威海泉悦旅游开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210628-08797",
                "accName": "重庆龙湖联新地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210629-08819",
                "accName": "武汉葛洲坝龙湖房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210629-08834",
                "accName": "重庆龙湖科恒地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210630-08878",
                "accName": "重庆龙湖创安地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210702-08910",
                "accName": "惠州市新耀忠置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210703-08917",
                "accName": "深圳市泰恒置地投资有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210704-08919",
                "accName": "贵州裕丰合置业投资有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210704-08922",
                "accName": "惠州市雅建房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210710-08998",
                "accName": "重庆龙湖鼎祥房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210712-09001",
                "accName": "重庆鼎升房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210712-09002",
                "accName": "重庆龙湖卓健房地产开发有限责任公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210712-09003",
                "accName": "重庆龙湖凯晟房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210713-09054",
                "accName": "重庆龙湖朗晟房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210717-09165",
                "accName": "福州鑫嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210720-09245",
                "accName": "重庆龙湖颐天展晟置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210721-09354",
                "accName": "云南江川仙湖锦绣旅游物业发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210723-09416",
                "accName": "南昌湖晟置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210729-09649",
                "accName": "福州德元房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210731-10837",
                "accName": "郑州龙兴房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210802-10870",
                "accName": "重庆龙湖恒宜房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210803-10872",
                "accName": "南京名骏置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210805-10904",
                "accName": "济南泰益房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210806-11046",
                "accName": "济南盛雪置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210806-11052",
                "accName": "济南泰瑞房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210807-11060",
                "accName": "济南泰盛房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210811-11113",
                "accName": "杭州龙孜投资管理有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210813-11187",
                "accName": "中山市永星置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210814-11202",
                "accName": "福建省大广汽车城发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210816-11213",
                "accName": "长沙江嵘置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210819-11323",
                "accName": "福州卓乔房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11376",
                "accName": "成都辰池置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11393",
                "accName": "成都龙湖锦城置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11394",
                "accName": "成都辰鉴置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11395",
                "accName": "成都辰崃置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11396",
                "accName": "成都希腾房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210820-11403",
                "accName": "成都辰迎置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210826-11953",
                "accName": "四川兴龙湖地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210826-11960",
                "accName": "天津睿吉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210902-12121",
                "accName": "重庆龙湖卓裕房地产开发有限责任公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210902-12130",
                "accName": "无锡市嘉融置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210907-12202",
                "accName": "龙湖物业服务集团有限公司昆明分公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210910-27181",
                "accName": "合肥锦淮房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210910-27516",
                "accName": "南京嘉腾置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210914-27965",
                "accName": "烟台新鸿宇置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28076",
                "accName": "上海恒固房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28083",
                "accName": "上海恒逸房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28084",
                "accName": "上海恒卓房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28085",
                "accName": "上海恒睿房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28086",
                "accName": "上海湖胤房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28087",
                "accName": "上海恒世房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28089",
                "accName": "苏州湖铭置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28090",
                "accName": "苏州合本投资管理有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28097",
                "accName": "苏州龙湖基业房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28105",
                "accName": "海南天街商业管理有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28111",
                "accName": "上海恒驰房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28112",
                "accName": "扬州市嘉昌置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210916-28164",
                "accName": "三亚市湖嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210917-28226",
                "accName": "珠海市卓轩房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210918-28403",
                "accName": "宁波龙尚房地产发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210926-29120",
                "accName": "合肥锦湖房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210927-29152",
                "accName": "江苏得昌置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210927-29154",
                "accName": "青岛胶澳华程置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210928-29244",
                "accName": "广州市君耀房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210928-29249",
                "accName": "广州福宝房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-210928-29250",
                "accName": "佛山市顺德区润嘉房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211002-29788",
                "accName": "常州市嘉信置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211015-34260",
                "accName": "云南嘉置置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211020-36248",
                "accName": "云南宜置置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211022-39229",
                "accName": "青岛万湖置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211026-39265",
                "accName": "青岛锦昊嘉辉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211028-39287",
                "accName": "温州龙耀健康产业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211028-39288",
                "accName": "苏州湖踞置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211029-39328",
                "accName": "青岛龙昊置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211102-39383",
                "accName": "青岛龙泰锦晖置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211103-39391",
                "accName": "青岛锦昊万华置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211104-39406",
                "accName": "青岛龙嘉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211104-39407",
                "accName": "青岛锦昊嘉煦置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211105-39425",
                "accName": "青岛龙凯置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211107-39445",
                "accName": "青岛馨梦园投资有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211108-39457",
                "accName": "成都辰明置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211109-39465",
                "accName": "莆田元景房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211109-39473",
                "accName": "成都辰璞置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211111-39481",
                "accName": "长春恒逸房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211112-39501",
                "accName": "烟台传化置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211112-39503",
                "accName": "济南中垠鑫熙置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211112-39512",
                "accName": "扬州市嘉腾置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211113-39533",
                "accName": "福州元顺房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211119-39657",
                "accName": "无锡市嘉栋置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211121-39666",
                "accName": "长春吉天房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39687",
                "accName": "威海市金猴龙昊置地有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39688",
                "accName": "惠州市天山祥和实业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39694",
                "accName": "成都景汇置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39695",
                "accName": "南京名万置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39696",
                "accName": "南宁龙湖金畅置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211124-39703",
                "accName": "珠海市润梁房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211125-39710",
                "accName": "郑州雅宸房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211125-39711",
                "accName": "郑州龙茂置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211126-39730",
                "accName": "长春嘉鑫房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211127-39737",
                "accName": "惠州市泛美置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211130-39821",
                "accName": "南京名贯置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211130-39824",
                "accName": "CRYSTAL SPHERE INVESTMENTS LIMITED-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211130-39928",
                "accName": "杭州龙诚房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211202-40186",
                "accName": "济南泰佳房地产开发有限责任公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211202-40199",
                "accName": "无锡嘉辉置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211208-40259",
                "accName": "CRYSTAL ACE GLOBAL LIMITED-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211208-40265",
                "accName": "常州嘉宜置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211208-40270",
                "accName": "成都龙湖北城置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211208-40276",
                "accName": "常州嘉悦置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211208-40285",
                "accName": "无锡市嘉正置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211210-40313",
                "accName": "龙湖物业服务集团有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211210-40320",
                "accName": "常州嘉博置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211212-40338",
                "accName": "青岛龙华盛锦置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211217-40465",
                "accName": "湛江市龙湖恩祥置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211220-40502",
                "accName": "长沙启顺房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211221-40527",
                "accName": "上海湖垚房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211223-40587",
                "accName": "福州市晋安区光正爱摩轮置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211223-40590",
                "accName": "重庆两江新区龙湖新卓佑房地产开发有限责任公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211223-40599",
                "accName": "长沙珑悦置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211224-40652",
                "accName": "南京名宏置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211224-40663",
                "accName": "深圳市熙梁投资发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211226-40684",
                "accName": "青岛龙泰晟德置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211228-40732",
                "accName": "福州盛嘉房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211230-40762",
                "accName": "杭州龙程房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-211230-40763",
                "accName": "云南锦博置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220106-40856",
                "accName": "绍兴龙坤房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220114-41044",
                "accName": "重庆龙湖舜允房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220127-42151",
                "accName": "肇庆市翼龙房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220214-42483",
                "accName": "赣州虔兴房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220215-42492",
                "accName": "南昌洪睦置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220216-42507",
                "accName": "济南龙湖置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220222-42575",
                "accName": "长沙顺盛房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220228-42632",
                "accName": "大连龙湖东港房地产有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220304-42703",
                "accName": "大连泽广置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220307-42722",
                "accName": "苏州首龙置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220307-42723",
                "accName": "苏州尚惠置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220307-42726",
                "accName": "苏州裕晖置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220307-42727",
                "accName": "苏州湖天置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220308-42920",
                "accName": "武汉清龙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220314-42962",
                "accName": "武汉园博园置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220314-42971",
                "accName": "云南嘉海置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220315-42972",
                "accName": "重庆龙湖怡和房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220315-42974",
                "accName": "重庆龙湖颐天鼎圣房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220316-42998",
                "accName": "大连金湾置地有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220318-43060",
                "accName": "南昌湖晟置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220320-43072",
                "accName": "威海市金猴龙昊置地有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220321-43074",
                "accName": "烟台传化置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220321-43079",
                "accName": "杭州龙郦实业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220322-43083",
                "accName": "南京名寓置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220326-43137",
                "accName": "重庆龙湖煦筑房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220331-43232",
                "accName": "宁德宇望房地产开发有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220401-43237",
                "accName": "南昌洪玺置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220402-43283",
                "accName": "成都龙湖锦川置业有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220406-43291",
                "accName": "无锡市嘉旭投资发展有限公司-C1客关活动激励-014"
            },
            {
                "accNo": "FF-220413-43341",
                "accName": "北京龙湖中佰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220414-43346",
                "accName": "贵阳龙湖度势文化产业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220414-43348",
                "accName": "重庆龙湖煦筑房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220415-43357",
                "accName": "苏州湖天置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220418-43401",
                "accName": "长沙江嵘置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220419-43416",
                "accName": "苏州裕晖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220420-43427",
                "accName": "长春吉天房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220420-43430",
                "accName": "合肥锦湖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220421-43432",
                "accName": "杭州龙誉投资管理有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220422-43444",
                "accName": "天津睿阳置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220425-43478",
                "accName": "中山市永星置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220426-43482",
                "accName": "烟台龙湖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43486",
                "accName": "郑州龙兴房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43490",
                "accName": "烟台上宸置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43491",
                "accName": "烟台中佰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43494",
                "accName": "惠州市新耀忠置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43496",
                "accName": "广州市君耀房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43503",
                "accName": "苏州湖铭置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43504",
                "accName": "苏州龙湖基业房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43505",
                "accName": "苏州合本投资管理有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43506",
                "accName": "苏州湖踞置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43507",
                "accName": "惠州市天山祥和实业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220427-43508",
                "accName": "惠州市泛美置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220428-43509",
                "accName": "深圳市泰恒置地投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220428-43512",
                "accName": "无锡市嘉栋置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220428-43514",
                "accName": "无锡嘉睿置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220428-43521",
                "accName": "海南天街商业管理有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220428-43522",
                "accName": "三亚市湖嘉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43545",
                "accName": "湛江市龙湖恩祥置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43550",
                "accName": "成都辰华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43551",
                "accName": "武汉市鑫呈捷房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43552",
                "accName": "重庆怡置龙湖弘茂房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43554",
                "accName": "重庆龙湖卓健房地产开发有限责任公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43556",
                "accName": "武汉晨鸣中利置业有限责任公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43557",
                "accName": "武汉龙嘉房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43561",
                "accName": "武汉尚龙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43564",
                "accName": "重庆鼎升房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220429-43567",
                "accName": "西安传化盛世地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220430-43568",
                "accName": "云南江川仙湖锦绣旅游物业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220430-43578",
                "accName": "西安龙湖众鑫置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220501-43581",
                "accName": "兰州兴耀置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220502-43586",
                "accName": "西安龙湖锦城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220503-43588",
                "accName": "长沙龙湖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220503-43589",
                "accName": "茂名市嘉逊置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220504-43591",
                "accName": "青岛馨梦园投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43592",
                "accName": "赣州虔兴房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43597",
                "accName": "苏州首龙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43599",
                "accName": "南通礴麒房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43601",
                "accName": "惠州市雅建房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43602",
                "accName": "沈阳龙湖新北置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43603",
                "accName": "郑州龙祥房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220505-43604",
                "accName": "青岛龙泰晟德置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220506-43612",
                "accName": "江苏得昌置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220507-43615",
                "accName": "嘉兴龙坤房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220507-43619",
                "accName": "重庆龙湖科恒地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220507-43620",
                "accName": "重庆龙湖宜祥地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220507-43623",
                "accName": "烟台龙湖物业服务有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220508-43625",
                "accName": "重庆龙湖创安地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220508-43630",
                "accName": "大连恒瑞房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220509-43678",
                "accName": "西安湖卓置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220510-43684",
                "accName": "重庆龙湖创佑地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43692",
                "accName": "济南泰瑞房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43693",
                "accName": "济南泰盛房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43694",
                "accName": "济南泰捷房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43695",
                "accName": "济南龙湖泰朗房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43696",
                "accName": "济南安齐房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43703",
                "accName": "南京名贯置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220511-43709",
                "accName": "杭州龙诚房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220512-43712",
                "accName": "福州盛元房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220513-43735",
                "accName": "龙湖物业服务集团有限公司昆明分公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220516-43760",
                "accName": "西安南湖锦腾置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220516-43761",
                "accName": "武汉中好汇科技有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220516-43764",
                "accName": "南宁龙湖金耀置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220516-43765",
                "accName": "重庆龙湖朗骏房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220516-43767",
                "accName": "武汉京文置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220517-43774",
                "accName": "西安天地国际时尚小镇房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220519-43799",
                "accName": "福州鑫嘉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220519-43806",
                "accName": "湛江市鑫鹏置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220523-43837",
                "accName": "青岛锦昊泰恒置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220523-43844",
                "accName": "成都辰启置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220524-43855",
                "accName": "重庆龙湖鼎祥房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220524-43863",
                "accName": "合肥锦河房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220525-43864",
                "accName": "济南泰佳房地产开发有限责任公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220525-43865",
                "accName": "济南盛雪置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220525-43869",
                "accName": "济南泰益房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220530-43910",
                "accName": "太原新城悦拓房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220531-43934",
                "accName": "长沙禧荣置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220531-43935",
                "accName": "青岛锦昊泰华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220531-43936",
                "accName": "青岛龙泽汇智置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220601-43953",
                "accName": "成都龙湖西城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220602-43956",
                "accName": "温州龙悦房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220602-43960",
                "accName": "咸阳盛湖华瀚置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220608-43988",
                "accName": "天津盛凯置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220608-43989",
                "accName": "天津鼎新置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220610-43995",
                "accName": "常州市嘉信置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220610-43997",
                "accName": "重庆龙湖联新地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220610-43998",
                "accName": "南宁龙湖金畅置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220613-44005",
                "accName": "重庆龙湖朗鑫房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220613-44006",
                "accName": "福州元昌房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220615-44011",
                "accName": "成都辰敏置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220616-44017",
                "accName": "济南泰晖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220616-44022",
                "accName": "大连金湾置地有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220616-44023",
                "accName": "常州市嘉邦置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220619-44047",
                "accName": "重庆两江新区龙湖新御置业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220621-44059",
                "accName": "青岛安洛惠庭置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220622-44067",
                "accName": "沈阳大华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220622-44068",
                "accName": "嘉兴龙晖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220623-44069",
                "accName": "莆田元景房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220623-44072",
                "accName": "南宁市渝银实业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220623-44073",
                "accName": "重庆龙湖恒宜房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220623-44074",
                "accName": "广州福宝房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220624-44077",
                "accName": "宁波龙湖置业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220624-44079",
                "accName": "重庆龙湖凯安地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220626-44082",
                "accName": "扬州市嘉昌置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220626-44083",
                "accName": "南宁龙湖卓景置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220627-44085",
                "accName": "长沙顺盛房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220627-44089",
                "accName": "温州龙浩房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220629-44092",
                "accName": "河北龙湖高远房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220630-44104",
                "accName": "济南中垠鑫熙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220630-44110",
                "accName": "济南龙湖泰然房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220706-44131",
                "accName": "西安龙湖航瑞置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220707-44137",
                "accName": "赣州锦誉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220707-44141",
                "accName": "西安龙湖兴城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220708-44142",
                "accName": "南京名辰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220708-44143",
                "accName": "南京嘉腾置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220708-44147",
                "accName": "青岛龙泰舜泽置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220709-44151",
                "accName": "重庆龙湖嘉旭地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220710-44154",
                "accName": "佛山市顺德区润嘉房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220713-44163",
                "accName": "桐乡市安鸿置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220714-44166",
                "accName": "无锡市嘉安置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220718-44209",
                "accName": "重庆龙湖成恒地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220721-44232",
                "accName": "福州兴元置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220721-44233",
                "accName": "贵州裕丰合置业投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220727-44277",
                "accName": "武汉锦顺置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220727-44278",
                "accName": "武汉清龙鑫荣置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220727-44279",
                "accName": "武汉厚德置业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220727-44280",
                "accName": "湖北龙合泰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220728-44287",
                "accName": "重庆龙湖景楠地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220729-44304",
                "accName": "贵阳兴龙湖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220801-44329",
                "accName": "天津睿吉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220801-44330",
                "accName": "天津龙湖睿海置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220803-44336",
                "accName": "重庆龙湖海成鼎鸿房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220804-44349",
                "accName": "常州嘉腾置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220810-44366",
                "accName": "无锡市嘉正置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220810-44368",
                "accName": "无锡市嘉融置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220815-44382",
                "accName": "重庆龙湖颐天鼎圣房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220815-44384",
                "accName": "绍兴龙坤房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220817-44390",
                "accName": "南京名万置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220818-44408",
                "accName": "济南泰鸿房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220819-44409",
                "accName": "南京嘉琇置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220819-44414",
                "accName": "南昌铃龙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220821-44422",
                "accName": "重庆龙湖舜允房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220822-44425",
                "accName": "南昌湖恒置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220824-44433",
                "accName": "武汉文泓置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220824-44435",
                "accName": "济南众龙置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220826-44441",
                "accName": "重庆龙湖卓裕房地产开发有限责任公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220826-44442",
                "accName": "青岛亿联龙盛投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220826-44443",
                "accName": "重庆龙湖颐天展晟置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220827-44445",
                "accName": "济南明茂置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220827-44446",
                "accName": "上海恒世房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220828-44448",
                "accName": "上海恒固房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220828-44449",
                "accName": "上海恒卓房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220828-44450",
                "accName": "上海恒睿房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220830-44453",
                "accName": "上海恒逸房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220830-44460",
                "accName": "上海恒驰房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220831-44489",
                "accName": "成都龙湖北城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220901-44490",
                "accName": "长沙启顺房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220903-44493",
                "accName": "南京名荣置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220907-44502",
                "accName": "无锡长裕置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44505",
                "accName": "北京龙和信泰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44507",
                "accName": "常州隆嘉实业投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44508",
                "accName": "烟台新鸿宇置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44509",
                "accName": "成都龙湖辰顺置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44512",
                "accName": "常熟湖虞置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220908-44513",
                "accName": "苏州湖泽置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220909-44523",
                "accName": "福州元辉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220909-44524",
                "accName": "宁德宇望房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220909-44525",
                "accName": "福州龙湖冠寓置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220909-44526",
                "accName": "福州宇冠置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220909-44527",
                "accName": "福清宇佳房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220910-44531",
                "accName": "威海市金猴置地有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220910-44532",
                "accName": "苏州华湖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220911-44535",
                "accName": "重庆龙湖怡置地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220913-44540",
                "accName": "重庆龙湖昕晖钰鑫房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220914-44541",
                "accName": "长沙龙佳置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220915-44547",
                "accName": "赣州锦坤置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220915-44548",
                "accName": "长沙奕盛置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220917-44574",
                "accName": "宁波龙兆房地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220919-44580",
                "accName": "沈阳吉天置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220919-44581",
                "accName": "长沙祺盛置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220919-44582",
                "accName": "长沙湖韵置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220920-44585",
                "accName": "长沙芙韵置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220920-44589",
                "accName": "南京名骏置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220920-44590",
                "accName": "重庆北龙湖置地发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220920-44591",
                "accName": "重庆嘉逊地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220920-44592",
                "accName": "重庆龙湖德卓地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220921-44597",
                "accName": "深圳市熙梁投资发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220921-44598",
                "accName": "重庆龙湖恒卓地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220922-44599",
                "accName": "宁波龙尚房地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220923-44602",
                "accName": "重庆龙湖地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220923-44606",
                "accName": "重庆龙湖朗晟房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220923-44607",
                "accName": "北京京珑置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220925-44613",
                "accName": "西安龙湖润融置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220926-44619",
                "accName": "宁波龙禧房地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220927-44623",
                "accName": "上海龙湖置业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220927-44624",
                "accName": "重庆龙湖企业拓展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220927-44628",
                "accName": "湛江市嘉辰置业投资有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220929-44659",
                "accName": "郑州雅泽房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220929-44661",
                "accName": "重庆龙湖昕晖鑫艺房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220929-44662",
                "accName": "郑州雅宸房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220930-44681",
                "accName": "广州市嘉万房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220930-44682",
                "accName": "重庆龙湖嘉博地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220930-44683",
                "accName": "郑州龙茂置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220930-44684",
                "accName": "南京名宏置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-220930-44686",
                "accName": "无锡市嘉旭投资发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221002-44692",
                "accName": "唐山兴佰俊泰房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221017-44725",
                "accName": "沈阳嘉佰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221018-44726",
                "accName": "青岛龙华盛锦置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221018-44743",
                "accName": "青岛龙泽嘉悦置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221018-44745",
                "accName": "北京滨湖恒兴房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221020-44752",
                "accName": "青岛龙逸置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221021-44764",
                "accName": "云南嘉置置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221021-44765",
                "accName": "成都辰鉴置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221021-44766",
                "accName": "北京中公未来教育科技有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221023-44777",
                "accName": "湖南壹捌捌壹置业发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221023-44778",
                "accName": "长沙经致置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221024-44781",
                "accName": "河北赢胜房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221025-44784",
                "accName": "长春市恒弘房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221028-44799",
                "accName": "河北领拓房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221101-44829",
                "accName": "肇庆市翼龙房地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221104-44836",
                "accName": "温州龙晖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221105-44839",
                "accName": "天津睿建置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221110-44845",
                "accName": "西安北城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221111-44851",
                "accName": "北京辰轩置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221111-44852",
                "accName": "北京尚泰信华房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221116-44866",
                "accName": "广州市璧湖房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221118-44886",
                "accName": "成都龙湖锦华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221118-44887",
                "accName": "成都龙湖同晋置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221118-44889",
                "accName": "天津睿渤置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221118-44890",
                "accName": "天津睿瀛置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221119-44891",
                "accName": "北京和顺安仁房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221119-44893",
                "accName": "天津兴润置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221121-44896",
                "accName": "唐山盟科房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221121-44898",
                "accName": "成都景汇置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221122-44899",
                "accName": "成都旭周置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221122-44900",
                "accName": "成都龙湖辰治置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221122-44903",
                "accName": "成都辰明置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221123-44905",
                "accName": "青岛锦昊睿达置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221123-44906",
                "accName": "成都龙湖锦鸿置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221124-44909",
                "accName": "北京葛洲坝龙湖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221125-44911",
                "accName": "成都龙湖锦城置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221128-44912",
                "accName": "青岛锦昊嘉辉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221129-44916",
                "accName": "成都辰崃置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221201-44959",
                "accName": "佛山市顺德区盛晖置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221205-44979",
                "accName": "青岛龙泰博睿置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221205-44981",
                "accName": "武汉安和盛泰房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221205-44982",
                "accName": "合肥龙湖地产有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221205-44984",
                "accName": "厦门龙湖德嘉置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221206-44986",
                "accName": "温州龙涛房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221206-44988",
                "accName": "西安旭晟置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221206-44989",
                "accName": "青岛金海优创置业有限公司-商业地块-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221207-44991",
                "accName": "云南宜置置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221209-45020",
                "accName": "北京盟科置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221209-45021",
                "accName": "晋中吉象恒逸房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221209-45024",
                "accName": "北京建邦锦泰置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221212-45040",
                "accName": "重庆龙湖创鑫房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221213-45055",
                "accName": "重庆龙湖景铭地产发展有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221214-45056",
                "accName": "北京龙湖庆华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221214-45057",
                "accName": "北京锦泰房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221214-45058",
                "accName": "北京龙湖兴顺置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221214-45062",
                "accName": "南昌洪睦置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221215-45065",
                "accName": "成都龙湖锦铭置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221215-45066",
                "accName": "成都旭府置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221215-45067",
                "accName": "成都西祥置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221216-45078",
                "accName": "成都旭蜀置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221216-45082",
                "accName": "成都辰池置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221219-45085",
                "accName": "沈阳红兴置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221219-45086",
                "accName": "沈阳嘉奕房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221220-45087",
                "accName": "成都汇新置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221220-45090",
                "accName": "北京锦昊万华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221221-45093",
                "accName": "成都辰琨置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221222-45103",
                "accName": "北京通瑞万华置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221222-45105",
                "accName": "北京龙湖时代置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221223-45117",
                "accName": "成都辰璞置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221224-45123",
                "accName": "成都嘉南置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221225-45126",
                "accName": "北京昭泰房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221228-45152",
                "accName": "昆明龙湖宜恒房地产开发有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-221228-45153",
                "accName": "成都西玺置业有限公司-C1客关活动激励-019"
            },
            {
                "accNo": "FF-201113-03181",
                "accName": "北京集顺工程咨询有限公司-C1运营服务号绑定激励-014"
            },
            {
                "accNo": "FF-210422-07339",
                "accName": "北京龙智工程咨询有限公司-C1运营服务号绑定激励-014"
            },
            {
                "accNo": "FF-211231-40799",
                "accName": "北京集顺工程咨询有限公司-C1运营服务号激励-014"
            },
            {
                "accNo": "QYFF-210820-11399",
                "accName": "掌乐积信息科技（重庆）有限公司-北京龙智工程咨询有限公司-129"
            },
            {
                "accNo": "QYFF-210820-11400",
                "accName": "掌乐积信息科技（重庆）有限公司-北京龙智数科科技服务有限公司-129"
            },
            {
                "accNo": "QYFF-210915-27972",
                "accName": "掌乐积信息科技（重庆）有限公司-大唐-南京欧亚航空客运代理有限公司-129"
            },
            {
                "accNo": "QYFF-211025-39250",
                "accName": "掌乐积信息科技（重庆）有限公司-易百信息技术（上海）股份有限公司-QY-422W-129"
            },
            {
                "accNo": "QYFF-211025-39254",
                "accName": "掌乐积信息科技（重庆）有限公司-中信银行股份有限公司信用卡中心-QY-356Q-129"
            },
            {
                "accNo": "QYFF-211129-39752",
                "accName": "掌乐积信息科技（重庆）有限公司-上海分互链信息技术有限公司-QY-092F-129"
            },
            {
                "accNo": "QYFF-220325-43133",
                "accName": "重庆珑珠信息科技有限公司-易百信息技术（上海）股份有限公司-QY-941B-129"
            },
            {
                "accNo": "QYFF-220520-43812",
                "accName": "重庆珑珠信息科技有限公司-北京集智数字科技有限公司-QY-974C-129"
            },
            {
                "accNo": "QYFF-220623-44070",
                "accName": "重庆珑珠信息科技有限公司-中信银行股份有限公司信用卡中心-QY-126K-129"
            },
            {
                "accNo": "QYFF-220623-44071",
                "accName": "重庆珑珠信息科技有限公司-中信银行股份有限公司信用卡中心-QY-498I-129"
            },
            {
                "accNo": "QYFF-221117-44872",
                "accName": "重庆珑珠信息科技有限公司-北京伊宸传媒文化有限公司-QY-231P-129"
            }
        ],
        "clearType": 1,
        "status": 1,
        "isDeleted": 0
    }

    for i in range(40):
        time.sleep(0.5)
        execute("/v1/accountFfClear/add", params)
