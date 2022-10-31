import requests


class REQ:
    def __init__(self):

        self.url = 'http://dbaexecsql.longfor.com/data_application/app_sqlquery/'

        self.head = {
            "Cookie": "CASTGC=TGT-195142-Wv0ZT-gR6tjr-6YfrCgEDHMj0NuurPtBOOW6bM5WkkecaoMM9NuDvDnGHaCba7OX-w8-longhu; account=TGT-195142-Wv0ZT-gR6tjr-6YfrCgEDHMj0NuurPtBOOW6bM5WkkecaoMM9NuDvDnGHaCba7OX-w8-longhu; sessionid=ja5pmhtlvysg1fphox5wtpup9vm9lxny",
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
