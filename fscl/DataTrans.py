import pymysql
import pandas as pd

# 创建一个MySQL数据库的连接对象
conn = pymysql.connect(
    host='210.65.47.53', port=3309,
    user='fashuichangliu', password='dklajgpi[wSOVkllkxcvnigrwewsd',
    charset='utf8mb4',database="fashuichangliu"
)

def readMasterData():

    ## 认识师父-资源表-封面
    insert_resource_sql = """
        INSERT INTO t_resource_inf (resource_url, resource_url_type, content, resource_type, create_time,
                            update_time, is_delete, title, name, area)
        SELECT concat(host,icon),0,'',3,now(6),now(6),0,category_name,'','' from understand_type ;
    """
    cursor = conn.cursor()
    cursor.execute(insert_resource_sql)
    conn.commit()

    select_resource_sql = """
        select id,title from t_resource_inf where is_delete = 0;
    """
    resource_map = {}
    conn_cursor = conn.cursor()
    conn_cursor.execute(select_resource_sql)
    fetchall = conn_cursor.fetchall()
    for index,col in enumerate(fetchall):
        resource_map[col[1]] = col[0]


    ## 认识师父-目录
    select_catalogue_master_sql = """
        select * from understand_type;
    """
    insert_catalogue_master_catalogue_sql = """
        INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
                                            update_time, operator, resource_count, img_id)
        VALUES ({0}, 0, {1}, {2}, {3}, 1, NOW(6), NOW(6), 'system', 0, {4});
    """
    conn_cursor = conn.cursor()
    conn_cursor.execute(select_catalogue_master_sql)
    fetchall = conn_cursor.fetchall()
    for col in fetchall:
        category_name = col[2]
        sort = col[5]
        if category_name == '認識法師':
            level = 1
            parent_id = 0
        else:
            level = 2
            conn_cursor.execute("select id from t_catalogue_inf where name = '認識法師'")
            parent_id = conn_cursor.fetchall()[0][0]
        conn_cursor.execute(insert_catalogue_master_catalogue_sql.format("'" +category_name + "'", level, sort, parent_id, resource_map[category_name]))
    conn.commit()

    #查询目录数据
    select_catalogue_sql = """
            select * from t_catalogue_inf;
        """
    cursor = conn.cursor()
    cursor.execute(select_catalogue_sql)
    cursor_fetchall = cursor.fetchall()
    catalogue_id_map = {}
    for item in cursor_fetchall:
        catalogue_id_map[item[1]] = item

    ## 认识师父-源数据
    select_comprehend_sql = """
        select * from comprehend;
    """
    cursor = conn.cursor()
    cursor.execute(select_comprehend_sql)
    comprehend_list = cursor.fetchall()

    ## 认识师父-资源
    insert_resource_master_sql = """
            INSERT INTO t_resource_inf (title, resource_url, resource_url_type, content, resource_type, name,
                                               area, is_delete, create_time, update_time)
            SELECT menu_name,null,null,menu_content,2,menu_name,null,0,NOW(6),NOW(6) from comprehend;
    """
    c = conn.cursor()
    c.execute(insert_resource_master_sql)
    conn.commit()

    ## 认识师父-内容
    insert_article_master_sql = """
            INSERT INTO t_article_inf (title, dict_level, catalogue_id, operator, status, templte_type, is_delete, is_topping,
                               sort, article_type, create_time, update_time, subscribe_num, admire_num, cover_resource_id)
            VALUES ({0}, {1}, {2}, 'system', 1, 1, 0, 0, {3}, 1, NOW(6), NOW(6), NULL,NULL, {4});
        """
    for index,item in enumerate(comprehend_list):
        title = "'" + item[3] + "'"
        sort = item[7]
        name = item[2]

        ## 如果该类型不存在
        cursor2 = conn.cursor()
        cursor2.execute("select * from t_catalogue_inf where name = {0}".format("'" + name + "'"))
        cursor__fetchall = cursor2.fetchall()
        if len(cursor__fetchall) < 1:
            cursor3 = conn.cursor()
            cursor3.execute(insert_catalogue_master_catalogue_sql.format("'" +name + "'", 2, 1, 1, -1))
            conn.commit()

        cursor4 = conn.cursor()
        cursor4.execute("select * from t_catalogue_inf where name = {0}".format("'" + name + "'"))
        fe_cursor4 = cursor4.fetchall()
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

def readTalkData():

    insert_catalogue_master_catalogue_sql = """
            INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
                                                update_time, operator, resource_count, img_id)
            VALUES ({0}, 0, {1}, {2}, {3}, 1, NOW(6), NOW(6), 'system', 0, {4});
        """

    ## 菁华开示-目录
    insert_catalogue_talk_catalogue_sql = """
            INSERT INTO t_catalogue_inf (name, belong, catalogue_level, sort, parent_id, status, create_time,
                                            update_time, operator, resource_count, img_id)
            SELECT amtb_type,5,1,list_index,0,1,NOW(6),now(6),'system',0,null from enlighttalktype;
        """
    conn_cursor = conn.cursor()
    conn_cursor.execute(insert_catalogue_talk_catalogue_sql)
    conn.commit()

    # 查询目录数据
    select_catalogue_sql = """
                select * from t_catalogue_inf where belong = 5;
            """
    cursor = conn.cursor()
    cursor.execute(select_catalogue_sql)
    cursor_fetchall = cursor.fetchall()
    catalogue_id_map = {}
    for item in cursor_fetchall:
        catalogue_id_map[item[1]] = item

    ## 菁华开示-源数据
    select_enlighttalk_sql = """
            select * from enlighttalk;
        """

    ## 菁华开示-源数据
    select_enlighttalk_type_sql = """
                select * from enlighttalk;
            """
    cursor = conn.cursor()
    cursor.execute(select_enlighttalk_sql)
    comprehend_list = cursor.fetchall()

    ## 菁华开示-资源
    insert_resource_master_sql = """
            INSERT INTO t_resource_inf (title, resource_url, resource_url_type, content, resource_type, name,
                                               area, is_delete, create_time, update_time)
            SELECT menu_name,null,null,menu_content,2,menu_name,null,0,NOW(6),NOW(6) from enlighttalk;
        """
    c = conn.cursor()
    c.execute(insert_resource_master_sql)
    conn.commit()

    ## 菁华开示-内容
    insert_article_master_sql = """
                INSERT INTO t_article_inf (title, dict_level, catalogue_id, operator, status, templte_type, is_delete, is_topping,
                                   sort, article_type, create_time, update_time, subscribe_num, admire_num, cover_resource_id)
                VALUES ({0}, {1}, {2}, 'system', 1, 1, 0, 0, {3}, 1, NOW(6), NOW(6), NULL,NULL, {4});
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
        conn.commit()

def insertDetail():
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


if __name__ == "__main__":

    # readMasterData()
    # readTalkData()
    #
    insertDetail()