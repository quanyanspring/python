import json
from concurrent.futures import ThreadPoolExecutor

import pymysql
import requests

import Config

# 创建一个MySQL数据库的连接对象
# conn_dev = pymysql.connect(
#     host='210.65.47.53', port=3309,
#     user='', password='',
#     charset='utf8mb4',database=""
# )

conn_prod = pymysql.connect(
    host='210.65.47.53', port=3309,
    user='fashuichangliunew', password='hvsVHDLfjoepqoweowuu2ehqdbaj',
    charset='utf8mb4',database="fashuichangliunew"
)

base_uurl = ""

"""
   认识师父 
"""
def readMasterData(conn):

    ## 认识师父-资源表-封面
    # insert_resource_sql = """
    #     INSERT INTO t_resource_inf (resource_url, resource_url_type, content, resource_type, create_time,
    #                         update_time, is_delete, title, name, area)
    #     SELECT concat(host,icon),0,'',3,now(6),now(6),0,category_name,'','' from understand_type ;
    # """
    # cursor = conn.cursor()
    # cursor.execute(insert_resource_sql)
    # conn.commit()

    # select_resource_sql = """
    #     select id,title from t_resource_inf where is_delete = 0;
    # """
    # resource_map = {}
    # conn_cursor = conn.cursor()
    # conn_cursor.execute(select_resource_sql)
    # fetchall = conn_cursor.fetchall()
    # for index,col in enumerate(fetchall):
    #     resource_map[col[1]] = col[0]


    ## 认识师父-目录
    # select_catalogue_master_sql = """
    #     select * from understand_type;
    # """
    # insert_catalogue_master_catalogue_sql = """
    #     INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
    #                                         update_time, operator, resource_count)
    #     VALUES ({0}, 0, {1}, {2}, {3}, 1, NOW(6), NOW(6), 'system', 0, {4});
    # """
    # conn_cursor = conn.cursor()
    # conn_cursor.execute(select_catalogue_master_sql)
    # fetchall = conn_cursor.fetchall()
    # for col in fetchall:
    #     category_name = col[2]
    #     sort = col[5]
    #     if category_name == '認識法師':
    #         level = 1
    #         parent_id = 0
    #     else:
    #         level = 2
    #         conn_cursor.execute("select id from t_catalogue_inf where name = '認識法師'")
    #         parent_id = conn_cursor.fetchall()[0][0]
    #     conn_cursor.execute(insert_catalogue_master_catalogue_sql.format("'" +category_name + "'", level, sort, parent_id))
    # conn.commit()

    #查询目录数据
    # select_catalogue_sql = """
    #         select * from t_catalogue_inf;
    #     """
    # cursor = conn.cursor()
    # cursor.execute(select_catalogue_sql)
    # cursor_fetchall = cursor.fetchall()
    # catalogue_id_map = {}
    # for item in cursor_fetchall:
    #     catalogue_id_map[item[1]] = item

    ## 认识师父-源数据
    select_comprehend_sql = """
        select * from comprehend;
    """
    cursor = conn.cursor()
    cursor.execute(select_comprehend_sql)
    comprehend_list = cursor.fetchall()

    ## 认识师父-资源
    # insert_resource_master_sql = """
    #         INSERT INTO t_resource_inf (title, resource_url, resource_url_type, content, resource_type, name,
    #                                            area, is_delete, create_time, update_time)
    #         SELECT menu_name,null,null,menu_content,2,menu_name,null,0,NOW(6),NOW(6) from comprehend;
    # """
    # c = conn.cursor()
    # c.execute(insert_resource_master_sql)
    # conn.commit()

    ## 认识师父-内容
    insert_article_master_sql = """
            INSERT INTO t_article_inf (title, dict_level, catalogue_id, operator, status, templte_type, is_delete, is_topping,
                               sort, article_type, create_time, update_time, subscribe_num, admire_num, cover_resource_id)
            VALUES ({0}, {1}, {2}, 'system', 1, 7, 0, 0, {3}, 0, NOW(6), NOW(6), NULL,NULL, {4});
        """
    for index,item in enumerate(comprehend_list):
        name = item[2]
        title = "'" + item[3] + "'"
        sort = item[7]

        ## 如果该类型不存在
        cursor2 = conn.cursor()
        cursor2.execute("select * from t_catalogue_inf where name = {0}".format("'" + name + "'"))
        cursor__fetchall = cursor2.fetchall()
        if len(cursor__fetchall) < 1:
            print("1")
            # cursor3 = conn.cursor()
            # cursor3.execute(insert_catalogue_master_catalogue_sql.format("'" +name + "'", 2, 1, 1, -1))
            # conn.commit()

        cursor4 = conn.cursor()
        cursor4.execute("select * from t_catalogue_inf where name = {0}".format("'" + name + "'"))
        fe_cursor4 = cursor4.fetchall()
        if len(cursor__fetchall) < 1:
            continue
        catalogue_id = fe_cursor4[0][0]
        dict_level = fe_cursor4[0][3]
        cover_resource_id = -1

        conn_cursor = conn.cursor()
        conn_cursor.execute(insert_article_master_sql.format(title,dict_level,catalogue_id,sort,cover_resource_id))
        conn.commit()

    # 认识师父-中间表
    inser_article_detail_master_sql = """
        INSERT INTO t_article_detail (article_id, resource_id, create_time, update_time, operator)
        SELECT f.id, i.id, NOW(6), NOW(6), 'system'
        FROM t_article_inf f
                 JOIN t_resource_inf i on f.title = i.title;
    """
    cursor1 = conn.cursor()
    cursor1.execute(inser_article_detail_master_sql)
    conn.commit()
"""
   菁华开示 
"""
def readTalkData(conn):

    # insert_catalogue_talk_catalogue_level_sql = """
    #         INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
    #                                         update_time, operator, resource_count, img_id)
    #         VALUES ('菁华开示', 0, 1, 50, 0, 1, NOW(6), NOW(6), 'system', null, null);
    #     """
    # conn_cursor = conn.cursor()
    # conn_cursor.execute(insert_catalogue_talk_catalogue_level_sql)
    # conn.commit()

    # select_catalogue_talk_catalogue_level_sql = """
    #         select * from t_catalogue_inf where name = '菁華開示';
    #     """
    # conn_cursor = conn.cursor()
    # conn_cursor.execute(select_catalogue_talk_catalogue_level_sql)
    # fe_all = conn_cursor.fetchall()
    # talk_catalogue_id = fe_all[0][0]

    ## 菁华开示-目录，后续需要修改belong = 5为1
    # insert_catalogue_talk_catalogue_sql = """
    #         INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
    #                                         update_time, operator, resource_count, img_id)
    #         SELECT amtb_type,5,1,list_index,{0},1,NOW(6),now(6),'system',0,null from enlighttalktype;
    #     """
    # conn_cursor = conn.cursor()
    # conn_cursor.execute(insert_catalogue_talk_catalogue_sql.format(talk_catalogue_id))
    # conn.commit()

    # 查询目录数据
    # select_catalogue_sql = """
    #             select * from t_catalogue_inf where belong = 5;
    #         """
    # cursor = conn.cursor()
    # cursor.execute(select_catalogue_sql)
    # cursor_fetchall = cursor.fetchall()
    # catalogue_id_map = {}
    # for item in cursor_fetchall:
    #     catalogue_id_map[item[1]] = item

    ## 菁华开示-资源
    insert_resource_master_sql = """
            INSERT INTO t_resource_inf (title, resource_url, resource_url_type, content, resource_type, name,
                                               area, is_delete, create_time, update_time)
            SELECT menu_name,null,null,menu_content,2,menu_name,null,0,NOW(6),NOW(6) from enlighttalk;
        """
    c = conn.cursor()
    c.execute(insert_resource_master_sql)
    conn.commit()

    ## 菁华开示-源数据
    select_enlighttalk_sql = """
                select * from enlighttalk;
            """
    cursor = conn.cursor()
    cursor.execute(select_enlighttalk_sql)
    comprehend_list = cursor.fetchall()

    ## 菁华开示-内容
    insert_article_master_sql = """
                INSERT INTO t_article_inf (title, dict_level, catalogue_id, operator, status, templte_type, is_delete, is_topping,
                                   sort, article_type, create_time, update_time, subscribe_num, admire_num, cover_resource_id)
                VALUES ({0}, {1}, {2}, 'system', 1, 7, 0, 0, {3}, 0, NOW(6), NOW(6), NULL,NULL, {4});
            """
    for index, item in enumerate(comprehend_list):
        title = "'" + item[2] + "'"
        sort = item[5]
        type_index = item[1]

        ## 如果该类型不存在
        cursor2 = conn.cursor()
        cursor2.execute("select i.id,i.catalogue_level from  enlighttalktype t join t_catalogue_inf i on i.name = t.amtb_type where t.amtb_index = {0}".format(type_index))
        cursor__fetchall = cursor2.fetchall()
        if len(cursor__fetchall) < 1:
            print(item)
            continue

        catalogue_id = cursor__fetchall[0][0]
        dict_level = cursor__fetchall[0][1]
        cover_resource_id = -1

        conn_cursor = conn.cursor()
        conn_cursor.execute(insert_article_master_sql.format(title, dict_level, catalogue_id, sort, cover_resource_id))
        if index % 5 == 0:
            conn.commit()
    conn.commit()

    # 菁华开示-中间表
    inser_article_detail_master_sql = """
            INSERT INTO t_article_detail (article_id, resource_id, create_time, update_time, operator)
            SELECT f.id, i.id, NOW(6), NOW(6), 'system'
            FROM t_article_inf f
                     JOIN t_resource_inf i on f.title = i.title ;
        """
    cursor1 = conn.cursor()
    cursor1.execute(inser_article_detail_master_sql)
    conn.commit()

"""
    统计目录文章数量
"""
def updateCatalogueCount(conn,article_type):
    select_article_count_sql = """
        select catalogue_id,count(*) from t_article_inf where is_delete = 0 and article_type = {0} group by catalogue_id;
    """
    update_catalogue_count_sql = """
        update t_catalogue_inf set resource_count = {0} where id = {1};
    """
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor1.execute(select_article_count_sql.format(article_type))
    fetchall = cursor1.fetchall()
    for col in fetchall:
        cursor2.execute(update_catalogue_count_sql.format(col[1],col[0]))
    conn.commit()

def updateParanterCatalogueCount(conn,article_type):
    select_article_count_sql = """
        select sum(resource_count) as result,parent_id from t_catalogue_inf where belong = 5 and parent_id != 0 group by parent_id;
    """
    update_catalogue_count_sql = """
        update t_catalogue_inf set resource_count = {0} where id = {1};
    """
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor1.execute(select_article_count_sql.format(article_type))
    fetchall = cursor1.fetchall()
    for col in fetchall:
        cursor2.execute(update_catalogue_count_sql.format(col[0],col[1]))
    conn.commit()

def readSourceSql(conn):
    file = open("/Users/wlq/Desktop/enlighttalk.sql", mode="r", encoding="utf-8")
    readlines = file.readlines()
    for index, item in enumerate(readlines):
        cursor1 = conn.cursor()
        cursor1.execute(item)
        if index % 5 == 0:
            conn.commit()
    conn.commit()

def invoke(params):

    split = str(params).split("-")

    server = "https://work.hwadzan.org/api/hwadzan/v2/medias/{0}/{1}"

    resp = requests.get(server.format(split[0],split[1]), timeout=1000)
    return resp.text

def sync_speech_task(conn,data_chunk,resouce_id_dict):

    # 请求接口
    detail = json.loads(invoke(data_chunk[0]))

    url = detail['jiangtanginfo']['subtable']['logo']

    if url is None or len(url) < 1:
        pass
    else:
        cover_url = base_uurl + url

        if cover_url in resouce_id_dict and data_chunk[1] == resouce_id_dict[cover_url]:
            print("跳过：%s" % data_chunk[0])
            pass
        else:
            cursor2 = conn.cursor()
            print("新增id = %s,url = %s, new_url = %s" % (data_chunk[0],data_chunk[2],cover_url))
            cursor2.execute(Config.insert_resource_sql.format("'" + data_chunk[0] + "'","'" + cover_url + "'", "'" + data_chunk[0] + "'"))
            lastId = cursor2.lastrowid
            print("返回 id = %s" % lastId)

            cursor3 = conn.cursor()
            cursor3.execute(Config.update_article_sql.format(lastId,data_chunk[3]))
            conn.commit()
            print("修改 id = %s" % data_chunk[3])

    print("完成 sourceId = %s" % data_chunk[0])

    conn.commit()

def task(data_chunk):
    sync_speech_task(con,data_chunk,resouce_id_dict)

def thread_pool_process(con):

    cursor = con.cursor()
    cursor.execute(Config.select_article_sql.format("'" + '01-000' + "'"))
    fetchall = cursor.fetchall()

    resouce_id_dict = {}
    for item in fetchall:
        resouce_id_dict[item[2]] = item[1]

    # 将数据集分成多个较小的分片
    num_threads = 8
    chunk_size = len(fetchall) // num_threads
    data_chunks = [fetchall[i:i + chunk_size] for i in range(0, len(fetchall), chunk_size)]

    # 创建线程池
    thread_pool = ThreadPoolExecutor(max_workers=num_threads)

    # 定义任务函数，用于处理每个分片的数据

    # 提交任务给线程池
    for chunk in data_chunks:
        thread_pool.submit(task(con,chunk,), chunk)

def syncSpeech(conn):
    select_article_sql = """
            select t.source_id, tt.id as resourceId, tt.resource_url, t.id as articleId
            from t_article_inf t
                     left join t_resource_inf tt on t.cover_resource_id = tt.id
            where t.article_type = 5
              and t.source_id > {0}
            order by t.source_id asc;
        """

    insert_resource_sql = """
               INSERT INTO t_resource_inf (title, resource_url, resource_url_type, invite_time, content, resource_type, name, area,
                            is_delete, source_type, create_time, update_time)
                VALUES ({0}, {1}, 0, null, null, 3, {2}, null, 0, 0,NOW(6), NOW(6));
            """

    update_article_sql = """
                  update t_article_inf set cover_resource_id = {0} where id = {1};
                """

    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    cursor1.execute(select_article_sql.format("'" + '32-117' + "'"))
    fetchall = cursor1.fetchall()

    resouceId_dict = {}
    for item in fetchall:
        resouceId_dict[item[2]] = item[1]

    for col in fetchall:

        detail = json.loads(invoke(col[0]))

        url = detail['jiangtanginfo']['subtable']['logo']

        if url is None or len(url) < 1:
            pass
        else:
            cover_url = base_uurl + url

            if cover_url in resouceId_dict and col[1] == resouceId_dict[cover_url]:
                print("跳过：%s" % col[0])
                pass
            else:
                print("新增id = %s,url = %s, new_url = %s" % (col[0],col[2],cover_url))
                cursor2.execute(insert_resource_sql.format("'" + col[0] + "'","'" + cover_url + "'", "'" + col[0] + "'"))
                lastId = cursor2.lastrowid
                print("返回 id = %s" % lastId)
                cursor3.execute(update_article_sql.format(lastId,col[3]))
                conn.commit()
                print("修改 id = %s" % col[3])

        print("完成 sourceId = %s" % col[0])

    conn.commit()

if __name__ == "__main__":

    #测试数据
    # db_info = conn_dev
    #生产数据
    db_info = conn_prod

    #导入源数据
    # readSourceSql(conn_prod)

    #认识师父
    # readMasterData(db_info)
    # 菁华开示
    # readTalkData(db_info)
    #统计文章数量
    # updateCatalogueCount(db_info,5)

    # updateParanterCatalogueCount(db_info,5)
    # thread_pool_process(conn_prod)
    
    syncSpeech(db_info)