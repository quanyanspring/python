import requests


class REQ:
    def __init__(self):

        self.url = 'http://dbaexecsql.longfor.com/data_application/app_sqlquery/'

        self.head = {
            "Cookie": "",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        # 请求数据
        self.data = {
            "instance_name": instance,
            "db_name": db_name,
            "schema_name": "",
            "tb_name": "",
            "sql_content": sql,
            "limit_num": 10000
        }

    def test(self):
        get = requests.post(self.url, self.head, self.data)
        print(get)


ewq = REQ()
ewq.test()
