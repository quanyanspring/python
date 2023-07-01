import concurrent.futures
from multiprocessing import cpu_count
from sqlalchemy import create_engine

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'database_name'
}

# 创建数据库连接池
engine = create_engine('mysql+pymysql://', pool_size=cpu_count(), **db_config)

# 线程处理函数
def query_database(query):
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.fetchall()

        # 打印查询结果
        print(f"Query: {query}")
        print("Result:")
        for row in rows:
            print(row)

# 创建线程池
with concurrent.futures.ThreadPoolExecutor() as executor:
    queries = ["SELECT * FROM table1", "SELECT * FROM table2", "SELECT * FROM table3"]

    # 提交任务给线程池
    results = [executor.submit(query_database, query) for query in queries]

    # 获取结果
    for future in concurrent.futures.as_completed(results):
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")
