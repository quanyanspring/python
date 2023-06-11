import threading
import requests
from openpyxl import Workbook


# 定义一个线程类
class RequestThread(threading.Thread):
    def __init__(self, url, data, result, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.result = result
        self.timeout = timeout

    def run(self):
        try:
            response = requests.post(self.url, json=self.data, timeout=self.timeout)
            self.result.extend(response.json())
        except requests.exceptions.Timeout:
            print(f"Request to {self.url} timed out.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {str(e)}")


# 创建多线程请求函数
def multi_threaded_requests(url, data_list, batch_size=10, timeout=10):
    result = []
    threads = []

    # 根据批次大小切分数据
    data_batches = [data_list[i:i + batch_size] for i in range(0, len(data_list), batch_size)]

    for data_batch in data_batches:
        thread = RequestThread(url, data_batch, result, timeout)
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    return result


# 模拟一批数据
data_list = [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Alice"},
    {"id": 3, "name": "Bob"},
    # 更多数据...
]

# 定义接口URL
url = "https://api.example.com/endpoint"

# 发起多线程请求，设置超时为5秒
results = multi_threaded_requests(url, data_list, batch_size=2, timeout=5)

# 将结果写入Excel文件
workbook = Workbook()
worksheet = workbook.active

# 写入表头
worksheet.append(["ID", "Name"])

# 写入结果集
for result in results:
    worksheet.append([result["id"], result["name"]])

# 保存Excel文件
workbook.save("results.xlsx")
